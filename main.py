from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.staticfiles import StaticFiles
from core.configs import settings
from api.v1.api import api_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx


app = FastAPI(title='WikiBel - Repertório de Belém')
app.include_router(api_router, prefix=settings.API_V1_SRT)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")#carregar o mapa de forma statica
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def view_mapa(request: Request):
    return templates.TemplateResponse("menu.html", {
        "request": request,
    })

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                     log_level="info", reload=True)
    

