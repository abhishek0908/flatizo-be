from bson import ObjectId
from beanie import Document
from pydantic import Field, constr
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from app.constants.property_enums import PropertyType, PreferenceType, FoodPreferenceType, ListingType
from beanie import Link
from app.models.user import User
from app.utils.mongo.pydantic_object import PyObjectId
class PropertyDetails(Document):
    property_uuid: UUID = Field(default_factory=uuid4, unique=True)
    name_of_property: constr(strip_whitespace=True, min_length=1)
    property_type: PropertyType 
    rent: float
    floor: Optional[str] = None
    description: str
    contact_number: constr(min_length=10, max_length=15, pattern=r"^\d{10,15}$")
    deposit: float
    images: List[str]
    user_id: PyObjectId  # Reference to User document
    gender_preference: PreferenceType
    listing_for : ListingType  # e.g., 'flatmate', 'owner'
    food_preference: FoodPreferenceType
    location: str

    class Settings:
        name = "property_details"