import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "database"))

# Ensure database directory exists
DATABASE_PATH.mkdir(parents=True, exist_ok=True)

# Security config
SECRET_KEY = os.getenv("SECRET_KEY", "campus_management_system_session_secret_key_2026")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "campus_management_system_jwt_secret_key_2026")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
