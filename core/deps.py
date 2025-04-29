from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.member_model import MemberModel

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()

    #Abrir e fechar a sessão com o banco de dados
    try:
        yield session
    finally:
        await session.close()

async def get_current_member(token: str, db: Session = Depends(get_session)) -> MemberModel:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(MemberModel).filter(MemberModel.id_u == int(token_data.username))
        result = await session.execute(query)
        member: MemberModel = result.scalars().unique_one_or_none()

        if member is None:
            raise credentials_exception

        return member