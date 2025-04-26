from fastapi import APIRouter
from api.v1.endpoints.mapa import router as mapa_router

api_router = APIRouter()
api_router.include_router(mapa_router, prefix="/mapa", tags=["Mapa"])
#Aqui adiciona as paginas criadas na pasta endpoints