# gemini/handlers.py
import asyncio
from io import BytesIO
from typing import Dict, List
import time

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
GENERATING_DOTS = [".", "..", "..."] # Pre-calculate dots

async def start_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n"
        "Start sending messages to generate a response.\n"
        "Send /new to start a new chat session."
    )


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Basic commands:\n"
        "/start - Start the bot\n"
        "/help - Display this help message\n\n"
        "Chat commands:\n"
        "/new - Start a new chat session"
    )
    await update.message.reply_text(help_text)


def initialize_chat_session(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["chat"] = model.start_chat()


async def new_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = await update.message.reply_text("Starting new chat session...")
    initialize_chat_session(context)
    await message.edit_text("New chat session started.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "chat" not in context.chat_data:
        initialize_chat_session(context)

    user_text = update.message.text
    feedback_message = await update.message.reply_text("Generating...")

    generating_task = asyncio.create_task(animate_generating(feedback_message))
    await update.message.chat.send_action(ChatAction.TYPING)

    chat_session = context.chat_data["chat"]
    start_time = time.time()

    try:
        response_chunks = await chat_session.send_message_async(user_text, stream=True)
        await stream_response_chunks(response_chunks, update)
    except (StopCandidateException, BlockedPromptException) as e:
        await handle_exception(e, user_text, feedback_message, chat_session)
    finally:
        generating_task.cancel()

    total_time = time.time() - start_time
    await update.message.reply_text(f"Total time taken: {total_time:.2f} seconds")


async def animate_generating(message, interval: float = 0.2) -> None:
    while True:
        for dot in GENERATING_DOTS:
            await message.edit_text(f"Generating{dot}")
            await asyncio.sleep(interval)


async def stream_response_chunks(response_chunks, update: Update) -> None:
    buffer = ""

    async for chunk in response_chunks:
        buffer += chunk.text or ""

        while len(buffer.encode('utf-8')) >= MAX_MESSAGE_SIZE:
            split_index = buffer[:MAX_MESSAGE_SIZE].rfind(' ') or MAX_MESSAGE_SIZE
            part, buffer = buffer[:split_index], buffer[split_index:].lstrip()

            if len(buffer.split()) <= WORD_ADJUSTMENT_THRESHOLD:
                part, buffer = f"{part} {buffer}", ""

            await send_message_part(update, part)

    if buffer:
        await send_message_part(update, buffer)


async def send_message_part(update: Update, message: str) -> None:
    formatted_message = format_message(message)
    await update.message.reply_text(
        formatted_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


async def handle_exception(e: Exception, user_text: str, message, chat_session) -> None:
    print(f"Exception with prompt '{user_text}': {e}")
    await message.edit_text("An issue occurred while generating a response.")
    chat_session.rewind()


async def handle_image(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    feedback_message = await update.message.reply_text(
        "Generating...", reply_to_message_id=update.message.message_id
    )

    highest_res_image = max(update.message.photo, key=lambda img: img.file_size)
    file = await highest_res_image.get_file()

    image_data = await file.download_as_bytearray()
    pil_image = load_image.open(BytesIO(image_data))

    prompt = update.message.caption or "Analyze this image and generate a response"

    try:
        response_chunks = await img_model.generate_content_async(
            [prompt, pil_image], stream=True
        )
        await stream_response_chunks_images(response_chunks, feedback_message)
    except StopCandidateException:
        await feedback_message.edit_text("The model unexpectedly stopped generating.")
    except NetworkError:
        await feedback_message.edit_text("Network error occurred. Please try again later.")
    except Exception as e:
        await feedback_message.edit_text(f"An unexpected error occurred: {e}")


# DRY
async def stream_response_chunks_images(response, feedback_message) -> None:
    full_message = ""

    async for chunk in response:
        if not chunk.text:
            continue

        full_message += chunk.text
        formatted_message = format_message(full_message)

        try:
            feedback_message = await feedback_message.edit_text(
                formatted_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )
        except BadRequest:
            continue

        await asyncio.sleep(0.1)


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Placeholder for handling audio messages.
    """
    pass
