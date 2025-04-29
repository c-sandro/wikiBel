from pytz import timezone

from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from models.member_model import MemberModel
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_SRT}/members/login"
)

async def authenticate_member(email: EmailStr, password: str, db: AsyncSession) -> Optional[MemberModel]:
    async with db as session:
        query = select(MemberModel).filter(MemberModel.email_u == email)
        result = await session.execute(query)
        member: MemberModel = result.scalars().unique().one_or_none()

        if not member:
            return None

        if not verify_password(password, member.password_u):
            return None

        return member

def _create_token(token_type: str, lifetime: timedelta, subject: str) -> str:
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expires = datetime.now(tz=sp) + lifetime

    payload['type'] = token_type
    payload['exp'] = expires
    #iat = issued at (quando foi gerado)
    payload['iat'] = datetime.now(tz=sp)
    payload['sub'] = str(subject)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(subject: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subject=subject
    )