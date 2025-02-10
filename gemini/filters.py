# gemini/filtes.py
import os
import logging
from telegram import Update
from telegram.ext.filters import UpdateFilter, COMMAND, TEXT, PHOTO, VOICE
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging for debugging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def get_authorized_users():
    """
    Retrieve authorized users from environment variables.
    Strips spaces and removes empty entries.

    Returns:
        frozenset: A set of authorized usernames and user IDs.
    """
    users = os.getenv("AUTHORIZED_USERS", "")
    authorized_users = frozenset(user.strip() for user in users.split(",") if user.strip())
    
    if not authorized_users:
        logger.warning("No authorized users specified. Allowing all users.")
    
    return authorized_users


class AuthorizedUserFilter(UpdateFilter):
    """Custom filter to check if a user is authorized."""

    def __init__(self, authorized_users):
        super().__init__()
        self.authorized_users = authorized_users

    def filter(self, update: Update) -> bool:
        """
        Check if the user is authorized based on username or user ID.

        Args:
            update: The Telegram update object.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        if not self.authorized_users:
            return True  # Allow all users if no restriction is set

        user = update.effective_user  # More reliable way to get the sender
        if not user:
            return False  # No user data available, reject by default

        return user.username in self.authorized_users or str(user.id) in self.authorized_users


# Retrieve authorized users once to avoid redundant calls
AUTHORIZED_USERS = get_authorized_users()

# Instance of the custom filter
auth_filter = AuthorizedUserFilter(AUTHORIZED_USERS)

# Predefined filters that combine authorization checks with specific message types

# MessageFilter: Authorized users' text messages that are not commands
message_filter = auth_filter & ~COMMAND & TEXT
# PhotoFilter: Authorized users' photo messages that are not commands
photo_filter = auth_filter & ~COMMAND & PHOTO
# AudioFilter: Authorized users' audio messages that are not commands
audio_filter = auth_filter & ~COMMAND & VOICE