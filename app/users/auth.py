from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.session_maker import SessionDep
from app.users.dao import UsersDAO
from app.auth.auth import verify_password
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings
from app.users.schemas import EmailModel

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str, session: AsyncSession = SessionDep):
    user = await UsersDAO.find_one_or_none(session=session, filters=EmailModel(email=email))
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


