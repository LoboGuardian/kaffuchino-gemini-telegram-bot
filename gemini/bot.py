# gemini/bot.py
import os
from functools import partial
from dotenv import load_dotenv
# Telegram
from telegram import Update
# Telegram ext
from telegram.ext import Application, CommandHandler, MessageHandler

from filters import auth_filter, message_filter, photo_filter, audio_filter
from handlers import start_command, help_command, new_chat_command, handle_message, handle_image


# Load environment variables from .env file
# Load environment variables only when needed
load_dotenv()
BOT_TOKEN_ENV = "BOT_TOKEN"
BOT_TOKEN = os.getenv(BOT_TOKEN_ENV)

if not BOT_TOKEN:
    raise ValueError(f"Missing environment variable: {BOT_TOKEN_ENV}")

# Command handlers mapping
COMMAND_HANDLERS = {
    "start_command": start_command,
    "help": help_command,
    "new": new_chat_command,
}

# Message handlers mapping
MESSAGE_HANDLERS = {
    message_filter: handle_message,
    photo_filter: handle_image,
}

# Use functools.partial to avoid redundant function definitions
add_handler = partial(CommandHandler, filters=auth_filter)

def create_application() -> Application:
    """Creates and configures the bot application."""
    application = Application.builder().token(BOT_TOKEN).build()

    for command, handler in COMMAND_HANDLERS.items():
        application.add_handler(add_handler(command, handler))

    for filter_, handler in MESSAGE_HANDLERS.items():
        application.add_handler(MessageHandler(filter_, handler))

    return application


# def add_authorized_handler(application, command, handler):
    # application.add_handler(CommandHandler(command,
                                        #    handler,
                                        #    filters=auth_filter))


def main() -> None:
    """Start the bot."""
    application = create_application()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # Create the Application and pass it your bot's token.
    # application = Application.builder().token(os.getenv(BOT_TOKEN_ENV)).build()

    # Register authorized command handlers from the COMMAND_HANDLERS dictionary
    # for command, handler in COMMAND_HANDLERS.items():
        # add_authorized_handler(application, command, handler)

    # Register message handlers for different content types
    # (text, images, audio).
    # application.add_handler(MessageHandler(message_filter, handle_message))
    # application.add_handler(MessageHandler(photo_filter, handle_image))
    # application.add_handler(MessageHandler(audio_filter, handle_audio))

    # Start the bot and enable listening for all update types.
    # It will run the bot until the user presses Ctrl-C
    # application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
