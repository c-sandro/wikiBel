from fastapi import APIRouter

#Aqui importa os endpoints
from api.v1.endpoints import member

api_router = APIRouter()
#Aqui adiciona as paginas criadas na pasta endpoints
api_router.include_router(member.router, prefix='/members', tags=["members"])