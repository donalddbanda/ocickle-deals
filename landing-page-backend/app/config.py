import os
from dotenv import load_dotenv
from .errors import MissingSecretKey

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise MissingSecretKey("Secret key is missing")