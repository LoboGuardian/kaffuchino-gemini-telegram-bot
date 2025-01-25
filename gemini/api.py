import os
import google.generativeai as genai
from google.generativeai.types.safety_types import (
    HarmCategory,
    HarmBlockThreshold
)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration to disable all safety filters for the Gemini models.
# This setting should be used with caution as it allows the models to generate
# potentially harmful content.
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
    HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_HARASSMENT:
    HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
    HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_HATE_SPEECH:
    HarmBlockThreshold.BLOCK_NONE,
}

# Configure the Google Generative AI API with the API key
# obtained from environment variables.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini text-based generative model with disabled
# safety settings.
#
# Using "gemini-2.0-flash-exp" model for faster text generation.
model = genai.GenerativeModel("gemini-2.0-flash-exp",
                              safety_settings=SAFETY_SETTINGS)

# Initialize the Gemini image-based generative model with disabled
# safety settings.
#
# Using "gemini-2.0-flash-exp" model for faster image processing and
# generation.
img_model = genai.GenerativeModel("gemini-2.0-flash-exp",
                                  safety_settings=SAFETY_SETTINGS)

# Note: The commented-out line below shows an alternative model for image
# processing, which was not chosen for this setup.
# img_model = genai.GenerativeModel("gemini-1.5-flash",
#                                   safety_settings=SAFETY_SETTINGS)
