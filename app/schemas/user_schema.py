from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginOTPRequest(BaseModel):
    email: EmailStr


class LoginOTPVerifyRequest(LoginOTPRequest):
    otp: str


class LoginOTPResponse(BaseModel):
    success: bool
    message: str


class LoginTokenResponse(BaseModel):
    success: bool
    message: str
    token: str


class UserInDB(LoginOTPRequest):
    id: Optional[str] = Field(None, alias="_id")
    user_uuid: str
    refreshToken: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
