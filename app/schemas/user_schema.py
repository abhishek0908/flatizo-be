from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginOTPRequest(BaseModel):
    email: EmailStr


class LoginOTPVerifyRequest(LoginOTPRequest):
    otp: str

class LoginOTPResponse(BaseModel):
    msg: str
class LoginTokenResponse(BaseModel):
    msg: str
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
