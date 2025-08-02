import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === File and Folder Paths ===
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# === OpenAI Settings ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# === Qdrant Vector DB Settings ===
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "documents")

# === App Settings ===
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".txt", ".bmp", ".tiff"]