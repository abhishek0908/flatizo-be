# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

class AppConfig:
    PORT = int(os.getenv("PORT", 4000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

class BrevoConfig:
    API_KEY = os.getenv("BREVO_API_KEY")

class JWTConfig:
    ACCESS_SECRET = os.getenv("JWT_ACCESS_TOKEN_SECRET")
    REFRESH_SECRET = os.getenv("JWT_REFRESH_TOKEN_SECRET")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

class MongoConfig:
    URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("MONGO_DB_NAME")

class RedisConfig:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    OTP_TTL = int(os.getenv("OTP_TTL", 300))

class AWSConfig:
    ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION = os.getenv("AWS_REGION")
    BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
