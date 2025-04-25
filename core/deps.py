from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()

    #Abrir e fechar a sessão com o banco de dados
    try:
        yield session
    finally:
        await session.close()