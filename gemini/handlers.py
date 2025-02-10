# gemini/handlers.py
import asyncio
import time
from io import BytesIO
from typing import Dict, List

# 
import PIL.Image as load_image

# Gemini local
from api import model, img_model
from parser import format_message
# Google Generative
from google.generativeai.types import GenerateContentResponse
from google.generativeai.types.generation_types import (
    StopCandidateException,
    BlockedPromptException,
)
# Telegram
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode


BUFFER_SIZE = 1024  # 1 KB
MAX_MESSAGE_SIZE = 2 * 1024  # 2 KB
WORD_ADJUSTMENT_THRESHOLD = 5  # Max words to adjust into previous message
GENERATING_DOTS = [".", "..", "...", "...."] # Pre-calculate dots

def _start_new_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Starts a new chat session by initializing a new chat object in the context.
    """
    context.chat_data["chat"] = model.start_chat()

async def start_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a welcome message to the user when the /start command is issued.
    """
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nStart sending messages to generate a response.\n\nSend /new to start a new chat session."
    )

async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a help message to the user when the /help command is issued."""
    help_text = """
        Basic commands:
        /start - Start the bot
        /help - Get help. Shows this message

        Chat commands:
        /new - Start a new chat session (model will forget previously
        generated messages)

        Send a message to the bot to generate a response.
        """
    await update.message.reply_text(help_text)


async def new_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Starts a new chat session and notifies the user.
    """
    init_msg = await update.message.reply_text("Starting new chat session...", reply_to_message_id=update.message.message_id)
    _start_new_chat(context)
    # init_msg = await update.message.reply_text(
        # text="Starting new chat session...",
        # reply_to_message_id=update.message.message_id,
    # )
    # _start_new_chat(context)
    await init_msg.edit_text("New chat session started.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming text messages from users.

    Initializes a chat session if it doesn't exist.
    Sends the user's message to the chat session to generate a response.
    Streams the response back to the user, handling various exceptions.
    """
    if "chat" not in context.chat_data:
        _start_new_chat(context)

    text = update.message.text
    init_msg = await update.message.reply_text("Generating", reply_to_message_id=update.message.message_id)

    async def update_generating_message():
        while True:
            for dot in GENERATING_DOTS:
                await init_msg.edit_text(f"Generating{dot}")
                await asyncio.sleep(0.2)
    
    generating_task = asyncio.create_task(update_generating_message())
    await update.message.chat.send_action(ChatAction.TYPING)

    chat = context.chat_data["chat"]
    start_time = time.time()

    try:
        response = await chat.send_message_async(text, stream=True)

    except (StopCandidateException, BlockedPromptException) as e:
        print(f"Error with prompt '{text}':", e)
        await init_msg.edit_text("An issue occurred while generating a response.")
        chat.rewind()
        generating_task.cancel()
        return

    buffer = ""
    # previous_part = ""
    # message_count = 1

    async for chunk in response:
        if chunk.text:
            buffer += chunk.text
            while len(buffer.encode('utf-8')) >= MAX_MESSAGE_SIZE:
                split_index = buffer[:MAX_MESSAGE_SIZE].rfind(' ')
                if split_index == -1:
                    split_index = MAX_MESSAGE_SIZE
                
                # part = buffer[:MAX_MESSAGE_SIZE]
                # buffer = buffer[MAX_MESSAGE_SIZE:]
                # part_kb = len(part) / 1024

                part = buffer[:split_index]
                buffer = buffer[split_index:].lstrip()
                
                # part_words = part.split()
                
                if len(buffer.split()) <= WORD_ADJUSTMENT_THRESHOLD:
                    part += " " + buffer
                    buffer = ""
                
                # part_kb = len(part.encode('utf-8')) / 1024
                # part_word_count = len(part.split())

                await update.message.reply_text(
                    f"{format_message(part)}",
                    # f"{format_message(part)}\nWord count: {part_word_count}",
                    # f"{format_message(part)}\nResponse size: {part_kb:.2f} KB",
                    # f"[Part {message_count}]\n{format_message(part)}\nResponse size: {part_kb:.2f} KB",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                # message_count += 1
                # await update.message.reply_text(f"{format_message(part)}", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                # await asyncio.sleep(0.1)

    generating_task.cancel()

    if buffer:
        # buffer_kb = len(buffer) / 1024
        # buffer_kb = len(buffer.encode('utf-8')) / 1024
        # buffer_word_count = len(buffer.split())

        await update.message.reply_text(
            f"{format_message(buffer)}",
            # f"{format_message(buffer)}\nWord count: {buffer_word_count}",
            # f"{format_message(buffer)}\nResponse size: {buffer_kb:.2f} KB",
            # f"[Part {message_count}]\n{format_message(buffer)}\nResponse size: {buffer_kb:.2f} KB",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        # await update.message.reply_text(f"{format_message(buffer)}", parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    end_time = time.time()
    total_time = end_time - start_time
    # buffer_kb = len(buffer) / 1024
    # stats_message = f"Response size: {len(buffer)} bytes\nTime taken: {end_time - start_time:.2f} seconds"
    await update.message.reply_text(f"Total time taken: {total_time:.2f} seconds")
    # stats_message = f"Response size: {buffer_kb:.2f} KB\nTime taken: {end_time - start_time:.2f} seconds"
    # await update.message.reply_text(stats_message)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming images with optional captions, generates a response using
    a model, and edits the initial message with the model's response.
    """
    init_msg = await update.message.reply_text("Generating...", reply_to_message_id=update.message.message_id)
    images = update.message.photo
    unique_images = _select_highest_resolution_image(images)
    file = await list(unique_images.values())[0].get_file()
    a_img = load_image.open(BytesIO(await file.download_as_bytearray()))
    prompt = update.message.caption or "Analyze this image and generate a response"
    response = await img_model.generate_content_async([prompt, a_img], stream=True)
    await _process_response_chunks(response, init_msg, update)

def _select_highest_resolution_image(images: List[any]) -> Dict[str, any]:
    """
    Selects the highest resolution version of each unique image,
    identified by its file_id (without last 7 chars).
    """
    unique_images = {}
    for img in images:
        file_id = img.file_id[:-7]
        if file_id not in unique_images or img.file_size > unique_images[file_id].file_size:
            unique_images[file_id] = img
    return unique_images


async def _process_response_chunks(response: GenerateContentResponse, init_msg: any, update: Update) -> None:
    """
    Processes chunks of a streamed response, updates the message
    with formatted text, and handles exceptions during response processing.
    """
    buffer = ""
    async for chunk in response:
        if chunk.text:
            buffer += chunk.text
            processed_buffer = False # Flag to track if buffer was processed in this iteration
            if len(buffer) >= BUFFER_SIZE:
                await init_msg.edit_text(
                    text=format_message(buffer),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                buffer = ""
                await asyncio.sleep(0.1)
    
    if buffer:
        await init_msg.edit_text(
            text=format_message(buffer),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Placeholder for handling audio messages.
    """
    pass
