"""
This module loads environment variables from a .env file for use throughout the application.

It retrieves database connection URIs, API keys, and authentication settings to ensure configuration
data is kept separate from the source code.
"""

import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
POSTGRES_URI = os.getenv("POSTGRES_URI")
DB_NAME = os.getenv("DB_NAME")
API_KEY = os.getenv("API_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))