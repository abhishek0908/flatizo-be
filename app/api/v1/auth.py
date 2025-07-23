from fastapi import APIRouter, HTTPException,status,Depends
from app.schemas.user_schema import LoginOTPVerifyRequest, LoginOTPRequest, LoginTokenResponse,LoginOTPResponse
from app.repositories.user_repo import get_user_repo
import logging
from app.repositories.user_repo import UserRepository,get_user_repo
from app.utils.otp.otp import generate_and_store_otp, verify_otp
from app.utils.security.jwt import JWTBearer, create_jwt_token
from app.tasks.email import send_otp_email_task
from app.models.user import User
router = APIRouter()

# Business Logic
@router.post("/login/request-otp",response_model=LoginOTPResponse)
async def request_otp(payload: LoginOTPRequest):
    try:
        otp: str = await generate_and_store_otp(payload.email)
        
        # Send OTP email directly
        send_otp_email_task.delay(
            recipient_email=payload.email,
            recipient_name="Ram",
            otp=otp
        )
        
        logging.info(f"OTP generated and sent to {payload.email}")
        return {"msg": "OTP sent successfully"}
        
    except Exception as e:
        logging.error(f"Failed to send OTP to {payload.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login/verify-otp",response_model=LoginTokenResponse)
async def verify_otp_route(
    payload: LoginOTPVerifyRequest,
    user_repo: UserRepository = Depends(get_user_repo)
):
    # 1. Verify OTP
    if not await verify_otp(payload.email, payload.otp):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
    # 2. Get or create user
    user = await user_repo.get_by_email(payload.email)
    if not user:
        user = await user_repo.create_user(payload.email)
        logging.info(f"New user created: {user.user_uuid} and {user.id}")
    else:
        logging.info(f"User logged in: {user.user_uuid} and {user.id}")
    # 3. Generate JWT token
    token = create_jwt_token({
        "sub": str(user.user_uuid),
        "email": user.email
    })
    return {"msg": "Login successful", "token": token}


async def get_current_user(
    token_payload: dict = Depends(JWTBearer()),
    user_repo: UserRepository = Depends(get_user_repo)
) -> User:
    user_uuid = token_payload.get("sub")
    user = await user_repo.get_current_user(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user