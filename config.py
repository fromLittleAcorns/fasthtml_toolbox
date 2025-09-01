"""
Configuration settings for User and Database module
"""

from pathlib import Path
import os

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Database configuration
DB_FILE = DATA_DIR / "project.db"
DB_CONFIG = {
    "database": str(DB_FILE)
}

# App config
APP_CONFIG = {
    "debug": True,
    "secret_key": os.getenv("SECRET_KEY", "your-very-long-random-secret-key-here-change-in-production"),
    "session_cookie": "fhtml_toolkit_cookie",
    "static_path": "static",
    
    # Claude API configuration
    "claude_api_key": os.getenv("CLAUDE_API_KEY"),
    "claude_model": "claude-sonnet-4-0",
    
    # File upload limits
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "allowed_file_types": [".csv", ".xlsx", ".xls"],
    
}
