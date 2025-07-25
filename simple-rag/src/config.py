import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Qdrant Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

# Helper: is this a cloud connection?
def is_cloud_qdrant():
    return QDRANT_API_KEY != "" and QDRANT_HOST.startswith("https://")

# For cloud, use QDRANT_URL; for local, use host/port
QDRANT_URL = QDRANT_HOST if is_cloud_qdrant() else None

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Document Processing
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Text Cleaning Configuration
REMOVE_STOPWORDS = os.getenv("REMOVE_STOPWORDS", "false").lower() == "true"
REMOVE_NUMBERS = os.getenv("REMOVE_NUMBERS", "false").lower() == "true"
CLEANING_LANGUAGE = os.getenv("CLEANING_LANGUAGE", "english") 