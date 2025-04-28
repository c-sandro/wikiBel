from sqlalchemy.ext.declarative import declarative_base

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #Configs gerais usadas no app

    #Caminho inicial das urls (talvez mude a cada versao?)
    API_V1_SRT: str = '/api/v1'

    #URL do banco de dados (senha => =<4H98:1ta>y(K4L;r0cOPL&?k9,V4w2M~[Jb4`ntOR%W&]+q#J69ebk&Y6&oDbL )
    DB_URL:str = "postgresql+asyncpg://wikibeldbmanager:=<4H98:1ta>y(K4L;r0cOPL&?k9,V4w2M~[Jb4`ntOR%W&]+q#J69ebk&Y6&oDbL@localhost:5432/wikibeldb"

    #Para todos os models possuirem os recursos do SQLAlchemy
    DBBaseModel = declarative_base

    #Senha da API, tipo de criptografia e tempo de acesso
    JWT_SECRET: str = 'EaY0WW0-TgF7kvkIxyJd-73pnGh_4mYrGRDgxt_g-Xk'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

#Instância da classe Settings pra usar onde necessário
settings = Settings()