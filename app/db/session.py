from app.models.properties_model import PropertyDetails
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from beanie import init_beanie
from app.models.user import User
import os
import logging
logger = logging.getLogger(__name__)
logger.info("This will be formatted as JSON if setup_logging() was called in main.py")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "flatizo")

client = AsyncIOMotorClient(MONGO_URL)
db: Database = client[MONGO_DB_NAME]

async def init_db():
    logger.info("Initializing database")
    await init_beanie(database=db, document_models=[User,PropertyDetails])
    logger.info("Database initialized")