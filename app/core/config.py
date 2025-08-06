import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 7))
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", 12))
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")

settings = Settings()