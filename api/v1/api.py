from fastapi import APIRouter
from api.v1.endpoints.mapa import router as mapa_router
from api.v1.endpoints.roteiro import router as roteiro_router
from api.v1.endpoints import member

api_router = APIRouter()
api_router.include_router(mapa_router, prefix="/mapa", tags=["Mapa"])
api_router.include_router(roteiro_router, prefix="/roteiro", tags=["Roteiro"])
#Aqui adiciona as paginas criadas na pasta endpoints


#Aqui adiciona as paginas criadas na pasta endpoints
api_router.include_router(member.router, prefix='/members', tags=["members"])
