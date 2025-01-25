import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
)

from gemini.filters import (
    auth_filter,
    message_filter,
    photo_filter,
    audio_filter
)

from gemini.handlers import (
    start_command,
    help_command,
    new_chat_command,
    handle_message,
    handle_image,
    handle_audio,
)

# Load environment variables from .env file
load_dotenv()

# Constants for command strings to avoid 'magic strings'
BOT_TOKEN_ENV = "BOT_TOKEN"
START_COMMAND = "start_command"
HELP_COMMAND = "help"
NEW_COMMAND = "new"

# A dictionary mapping command strings to their respective handler functions
COMMAND_HANDLERS = {
    START_COMMAND: start_command,
    HELP_COMMAND: help_command,
    NEW_COMMAND: new_chat_command,
}


def add_authorized_handler(application, command, handler):
    application.add_handler(CommandHandler(command,
                                           handler,
                                           filters=auth_filter))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv(BOT_TOKEN_ENV)).build()

    # Register authorized command handlers from the COMMAND_HANDLERS dictionary
    for command, handler in COMMAND_HANDLERS.items():
        add_authorized_handler(application, command, handler)

    # Register message handlers for different content types
    # (text, images, audio).
    application.add_handler(MessageHandler(message_filter, handle_message))
    application.add_handler(MessageHandler(photo_filter, handle_image))
    application.add_handler(MessageHandler(audio_filter, handle_audio))

    # Start the bot and enable listening for all update types.
    # It will run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
