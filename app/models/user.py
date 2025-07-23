from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class User(Document):
    user_uuid: UUID = Field(default_factory=uuid4)
    name: Optional[str] = None
    email: EmailStr  # required (permanent)
    phoneNumber: Optional[str] = Field(
        default=None, min_length=10, max_length=10, pattern=r"^\d{10}$"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

        