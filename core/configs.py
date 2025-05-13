from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, ClassVar
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configs gerais usadas no app
    """
    # Caminho inicial das URLs (talvez mude a cada versão?)
    API_V1_SRT: str = '/api/v1'
    GOOGLE_MAPS_API_KEY: str
    GEMINI_API_KEY: str

    # URL do banco de dados
    DB_URL: str = "postgresql://wikibeldbmanager:=<4H98:1ta>y(K4L;r0cOPL&?k9,V4w2M~[Jb4`ntOR%W&]+q#J69ebk&Y6&oDbL@localhost:5432/wikibeldb"

    # Para todos os models possuírem os recursos do SQLAlchemy
    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True
        env_file = ".env"

# Instância da classe Settings pra usar onde necessário
settings = Settings()
