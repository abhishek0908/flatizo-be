from typing import Optional
from app.models.user import User
from datetime import datetime

# Hnadle to talk with db
class UserRepository:
    async def get_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_current_user(self, user_uuid: str) -> Optional[User]:
        from uuid import UUID
        try:
            uuid_val = UUID(user_uuid)
        except Exception:
            return None
        return await User.find_one(User.user_uuid == uuid_val)

    async def create_user(self, email: str) -> User:
        user = User(email=email)
        return await user.insert()

    async def update_last_login(self, user: User):
        user.last_login = datetime.utcnow()
        await user.save()
user_repo = UserRepository()

def get_user_repo():
    return user_repo