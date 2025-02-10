# gemini/api.py
import os
import google.generativeai as genai
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration to disable all safety filters for the Gemini models.
# This setting should be used with caution as it allows the models to generate
# potentially harmful content.
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,

    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
}

# Configure the Google Generative AI API with the API key
# obtained from environment variables.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Error: Environment variable 'GOOGLE_API_KEY' is not defined")

# Configure the Google Generative AI API
genai.configure(api_key=GOOGLE_API_KEY)


# Define the model to use (if you want to change it, just modify it here)
# Using "gemini-2.0-flash-exp" model for faster text generation.
# - gemini-1.5-flash: Lightweight model optimized for tasks where speed and efficiency are crucial.
# - gemini-1.5-pro: Advanced model for reasoning on large amounts of data.
# - gemini-2.0-flash: Powerful model with low latency and improved throughput, ideal for agentic experiences.
# - gemini-2.0-flash-lite: Cost-effective model with improved efficiency and expanded context window.
# - gemini-2.0-pro: Our best model to date for performance on complex coding and prompts.
# - gemini-2.0-flash-thinking: Improved model for reasoning, capable of displaying its thoughts to improve performance and explainability.
# - gemini-1.0-ultra: Our largest model for highly complex tasks.
# - gemini-1.0-nano: Efficient model for tasks on local devices.
# - gemini-2.0-flash-lite-preview-02-05
# - gemini-2.0-pro-exp-02-05
# - gemini-2.0-flash-thinking-exp-01-21


# Available models:
# GEMMA Models:
# - gemma-2-2b-it: A lightweight model optimized for small-scale tasks with efficiency.
# - gemma-2-9b-it: A mid-size model offering a balance between efficiency and performance.
# - gemma-2-27b-it: A powerful model for advanced reasoning and high-complexity tasks.

# GEMINI 1.5 Models:
# - gemini-1.5-pro: A robust model for complex reasoning and large-scale information processing.
# - gemini-1.5-flash: A lightweight and optimized model for fast responses and low latency.
# - gemini-1.5-flash-8b: An optimized variant of Flash with better balance between performance and speed.

# PREVIEW (Experimental) Models:
# - gemini-2.0-flash-exp: An experimental version of Gemini 2.0 Flash, designed for testing new capabilities.
# - learnlm-1.5-pro-experimental: An experimental model focused on learning-related applications.

# GEMINI 2.0 Models:
# - gemini-2.0-flash: The official Gemini 2.0 Flash model, optimized for high-speed text generation.
# - gemini-2.0-flash-lite-preview-02-05: A preview version of a cost-efficient and lightweight Flash variant.
# - gemini-2.0-pro-exp-02-05: An experimental version of Gemini 2.0 Pro with improved performance.
# - gemini-2.0-flash-thinking-exp-01-21: An experimental Flash model designed to improve reasoning by explaining its thought process.

# MODEL_NAME = "gemini-2.0-pro-exp-02-05"
MODEL_NAME = "gemini-2.0-flash-thinking-exp-01-21"

# Initialize the Gemini text-based generative model with disabled
# safety settings.
def initialize_model(model_name: str) -> genai.GenerativeModel:
    """Inicializa y devuelve un modelo generativo de Google AI."""
    return genai.GenerativeModel(model_name, safety_settings=SAFETY_SETTINGS)

# Inicializar modelos para texto e imágenes
model = initialize_model(MODEL_NAME)
img_model = initialize_model(MODEL_NAME)