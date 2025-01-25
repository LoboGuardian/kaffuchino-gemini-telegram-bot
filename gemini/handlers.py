import asyncio
from io import BytesIO
from typing import Dict, List

import PIL.Image as load_image
from gemini.api import model, img_model
from gemini.parser import format_message
from google.generativeai.types import GenerateContentResponse
from google.generativeai.types.generation_types import (
    StopCandidateException,
    BlockedPromptException,
)
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode


def _start_new_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Starts a new chat session by initializing a new chat object
    in the context.
    """
    context.chat_data["chat"] = model.start_chat()


async def start_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a welcome message to the user when the /start command is issued.
    """
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nStart sending messages with me to \
        generate a response.\n\nSend /new to start a new chat session.",
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


async def new_chat_command(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts a new chat session and notifies the user."""
    init_msg = await update.message.reply_text(
        text="Starting new chat session...",
        reply_to_message_id=update.message.message_id,
    )
    _start_new_chat(context)
    await init_msg.edit_text("New chat session started.")


async def handle_message(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming text messages from users.

    Initializes a chat session if it doesn't exist.
    Sends the user's message to the chat session to generate a response.
    Streams the response back to the user, handling various exceptions.
    """

    # Initialize chat if not already present
    if "chat" not in context.chat_data:
        _start_new_chat(context)

    # if context.chat_data.get("chat") is None:
        # _start_new_chat(context)

    text = update.message.text
    init_msg = await update.message.reply_text(
        text="Generating...", reply_to_message_id=update.message.message_id
    )
    await update.message.chat.send_action(ChatAction.TYPING)

    # Generate a response using the text-generation pipeline
    chat = context.chat_data["chat"]  # Get the chat session for this chat
    response = None
    try:
        response = await chat.send_message_async(
            text, stream=True
        )  # Generate a response
    except StopCandidateException as sce:
        print("Prompt:", text, "was stopped. User:", update.message.from_user)
        print(sce)
        await init_msg.edit_text("The model unexpectedly stopped generating.")
        chat.rewind()  # Reset chat session to avoid stuck state
        return
    except BlockedPromptException as bpe:
        print("Prompt:", text, "was blocked. User:", update.message.from_user)
        print(bpe)
        await init_msg.edit_text("Blocked due to safety concerns.")
        if response:
            await response.resolve()  # Resolve to free resources
        return

    full_plain_message = ""
    # Stream and process the response
    try:
        async for chunk in response:
            if not chunk.text:
                continue  # Skip empty chunks

            full_plain_message += chunk.text
            message = format_message(full_plain_message)
            init_msg = await init_msg.edit_text(
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            await asyncio.sleep(0.1)  # Prevent rate-limiting

    except StopCandidateException:
        await init_msg.edit_text("The model unexpectedly stopped generating.")
        chat.rewind()  # Reset chat session to avoid stuck state
    except BadRequest:
        if response:
            await response.resolve()  # Resolve to free resources
    except NetworkError:
        raise NetworkError(
            "Looks like your network is down. Please try again later."
        )
    except IndexError:
        await init_msg.reply_text(
            "Some index error occurred. This response is not supported."
        )
        if response:
            await response.resolve()  # Resolve to free resources
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if full_plain_message:
            message = format_message(full_plain_message)
            await update.message.reply_text(
                text=message,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=init_msg.message_id,
                disable_web_page_preview=True,
            )


async def handle_image(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming images with optional captions, generates a response using
    a model, and edits the initial message with the model's response.
    """

    init_msg = await update.message.reply_text(
        text="Generating...", reply_to_message_id=update.message.message_id
    )

    images = update.message.photo
    unique_images: Dict[str, any] = _select_highest_resolution_image(images)
    file_list: List[any] = list(unique_images.values())

    file = await file_list[0].get_file()
    image_bytes = await file.download_as_bytearray()
    a_img = load_image.open(BytesIO(image_bytes))

    prompt = (
       update.message.caption
       if update.message.caption
       else "Analyze this image and generate a response"
    )

    response = await img_model.generate_content_async([prompt, a_img],
                                                      stream=True)
    full_plain_message = ""
    await _process_response_chunks(response, init_msg, full_plain_message,
                                   update)


def _select_highest_resolution_image(images: List[any]) -> Dict[str, any]:
    """
    Selects the highest resolution version of each unique image,
    identified by its file_id (without last 7 chars).
    """
    unique_images: Dict[str, any] = {}
    for img in images:
        file_id = img.file_id[:-7]
        if file_id not in unique_images:
            unique_images[file_id] = img
        elif img.file_size > unique_images[file_id].file_size:
            unique_images[file_id] = img
    return unique_images


async def _process_response_chunks(
    response: GenerateContentResponse,
    init_msg: any,
    full_plain_message: str,
    update: Update,
) -> None:
    """
    Processes chunks of a streamed response, updates the message
    with formatted text, and handles exceptions during response processing.
    """
    try:
        async for chunk in response:
            if chunk.text:
                full_plain_message += chunk.text
                message = format_message(full_plain_message)
                init_msg = await init_msg.edit_text(
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            await asyncio.sleep(0.1)  # Avoid Flood
    except StopCandidateException:
        await init_msg.edit_text("The model unexpectedly stopped generating.")
    except BadRequest:
        await response.resolve()
    except NetworkError:
        raise NetworkError(
                "Looks like you're network is down. Please try again later."
            )
    except IndexError:
        await init_msg.reply_text(
            "Some index error occurred. This response is not supported."
        )
        await response.resolve()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if chunk.text:
            full_plain_message = chunk.text
            message = format_message(full_plain_message)
            await update.message.reply_text(
                text=message,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=init_msg.message_id,
                disable_web_page_preview=True,
            )


async def handle_audio(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
