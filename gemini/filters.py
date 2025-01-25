import os
from telegram import Update
from telegram.ext.filters import UpdateFilter, COMMAND, TEXT, PHOTO, VOICE
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get authorized user IDs/usernames, strip spaces, and remove empty strings
_AUTHORIZED_USERS = [
    user.strip()
    for user in os.getenv("AUTHORIZED_USERS", "").split(",")
    if user.strip()
]


class AuthorizedUserFilter(UpdateFilter):
    """Custom filter to check if a user is authorized."""

    def filter(self, update: Update) -> bool:
        """
        Check if the user is authorized based on username or user ID.

        Args:
            update: The Telegram update object.

        Returns:
             True if the user is authorized, False otherwise.
        """
        # If no authorized users are defined, allow all users
        if not _AUTHORIZED_USERS:
            return True
        # Check if the message sender's username or ID is in the
        # authorized list
        return (
            update.message.from_user.username in _AUTHORIZED_USERS
            or str(update.message.from_user.id) in _AUTHORIZED_USERS
        )


# Instance of the custom filter for easy use
auth_filter = AuthorizedUserFilter()

# Predefined filters that combine authorization check with
# specific message types

# MessageFilter: Authorized users' text messages that are not commands
message_filter = auth_filter & ~COMMAND & TEXT
# PhotoFilter: Authorized users' photo messages that are not commands
photo_filter = auth_filter & ~COMMAND & PHOTO
# AudioFilter: Authorized users' audio messages that are not commands
audio_filter = auth_filter & ~COMMAND & VOICE
