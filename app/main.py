from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from app.api.v1 import auth, properties
from app.db.session import init_db
from app.config.logging_config import setup_logging

setup_logging()
app = FastAPI(title="Flatizo - Flat Listing App")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(properties.router, prefix="/api/v1/flats", tags=["Flats"])


@app.on_event("startup")
async def on_startup():
    await init_db()
