# OTP generation/validation helpers moved from utils/otp.py

import secrets
import redis.asyncio as redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
OTP_TTL = int(os.getenv("OTP_TTL", "300"))  # seconds (5 minutes)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def generate_and_store_otp(email: str) -> str:
    otp = str(secrets.randbelow(10**6)).zfill(6)
    await redis_client.set(f"otp:{email}", otp, ex=OTP_TTL)
    return otp

async def verify_otp(email: str, otp: str) -> bool:
    stored_otp = await redis_client.get(f"otp:{email}")
    if stored_otp == otp:
        await redis_client.delete(f"otp:{email}")  # Invalidate after use
        return True
    return False
