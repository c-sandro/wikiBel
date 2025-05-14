from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

from core.configs import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Chave da API do Google Maps
GOOGLE_MAPS_API_KEY = settings.GOOGLE_MAPS_API_KEY

# Rota para geocodificação
@router.get("/geocode")
async def geocode(endereco: str = Query(..., description="Endereço")):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": endereco,
        "key": GOOGLE_MAPS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    return data

# Rota para visualização do mapa
@router.get("/view", response_class=HTMLResponse)
async def view_mapa(request: Request):
    return templates.TemplateResponse("mapa.html", {
        "request": request,
        "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
    })
