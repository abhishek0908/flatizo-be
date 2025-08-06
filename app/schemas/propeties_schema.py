from pydantic import BaseModel
from typing import Optional, List
from app.models.properties_model import PropertyDetails
from app.models.user import User
from app.constants.property_enums import (
    PropertyType,
    PreferenceType,
    FoodPreferenceType,
    ListingType,
)
from uuid import UUID
from app.utils.mongo.pydantic_object import PyObjectId
from fastapi import Form


class PropertyDetailsBase(BaseModel):
    name_of_property: str
    property_type: PropertyType
    rent: float
    floor: Optional[str] = None
    description: str
    contact_number: str
    deposit: float
    gender_preference: PreferenceType
    listing_for: ListingType
    food_preference: FoodPreferenceType
    location: str


class PropertyDetailsAll(BaseModel):
    name_of_property: str
    property_type: PropertyType
    rent: float
    floor: Optional[str] = None
    description: str
    contact_number: str
    deposit: float
    gender_preference: PreferenceType
    listing_for: ListingType
    food_preference: FoodPreferenceType
    location: str
    images: List[str] = []


class PropertyDetailsCreate(PropertyDetailsBase):
    user_id: PyObjectId
    images: List[str] = []
    model_config = {"arbitrary_types_allowed": True}


class PropertyDetailsUpdate(BaseModel):
    name_of_property: Optional[str] = None
    property_type: Optional[PropertyType] = None
    rent: Optional[float] = None
    floor: Optional[str] = None
    description: Optional[str] = None
    contact_number: Optional[str] = None
    deposit: Optional[float] = None
    images: Optional[List[str]] = None
    gender_preference: Optional[PreferenceType] = None
    listing_for: Optional[ListingType] = None
    food_preference: Optional[FoodPreferenceType] = None
    location: Optional[str] = None


class PropertyDetailsRead(PropertyDetailsBase):
    property_uuid: UUID
    user: UUID


class PropertyDetailsForm(BaseModel):
    name_of_property: str
    property_type: PropertyType
    rent: float
    floor: Optional[str] = None
    description: str
    contact_number: str
    deposit: float
    gender_preference: PreferenceType
    listing_for: ListingType
    food_preference: FoodPreferenceType
    location: str

    @classmethod
    def as_form(
        cls,
        name_of_property: str = Form(...),
        property_type: PropertyType = Form(...),
        rent: float = Form(...),
        floor: Optional[str] = Form(None),
        description: str = Form(...),
        contact_number: str = Form(...),
        deposit: float = Form(...),
        gender_preference: PreferenceType = Form(...),
        listing_for: ListingType = Form(...),
        food_preference: FoodPreferenceType = Form(...),
        location: str = Form(...),
    ) -> "PropertyDetailsForm":
        return cls(
            name_of_property=name_of_property,
            property_type=property_type,
            rent=rent,
            floor=floor,
            description=description,
            contact_number=contact_number,
            deposit=deposit,
            gender_preference=gender_preference,
            listing_for=listing_for,
            food_preference=food_preference,
            location=location,
        )
