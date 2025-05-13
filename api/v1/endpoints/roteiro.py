from fastapi import APIRouter, Query, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse

from core.configs import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
genai.configure(api_key=settings.GEMINI_API_KEY)


class ModeloRoteiroLongo(BaseModel):
    data_inicio: str
    data_fim: str
    preferencias: list[str] = []

class ModeloRoteiroCurto(BaseModel):
    hora_inicio: str
    hora_fim: str
    preferencias: list[str] = []


@router.get("/gerarroteirolongo", response_class=HTMLResponse)
async def gerar_roteiro_form_get(request: Request):
    return templates.TemplateResponse("gerar_roteiro_longo.html", {"request": request})

@router.get("/gerarroteirocurto", response_class=HTMLResponse)
async def gerar_roteiro_form_get(request: Request):
    return templates.TemplateResponse("gerar_roteiro_curto.html", {"request": request})


@router.post("/gerar-roteiro-longo/")
async def gerar_roteiro_longo(req: ModeloRoteiroLongo):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    if req.data_inicio > req.data_fim:
       response = "Estas datas são inválidas, favor inserir novamente."
       return JSONResponse(content={"erro": response}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    response = model.generate_content(
        f"crie um guia turístico detalhado para Belém do Pará entre os dias {req.data_inicio} e {req.data_fim}, "
         f"sendo estritamente importante levar em consideração essas preferências: {', '.join(req.preferencias)}, "
        "liste as atividades por dia, com sugestões clássicas de guias de turismo, como restaurantes sugeridos, atrações, celebrações e deslocamento."
    )
    return JSONResponse(content={"roteiro": response.text})




@router.post("/gerar-roteiro-curto/")
async def gerar_roteiro_longo(req: ModeloRoteiroCurto):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    if req.hora_inicio > req.hora_fim:
       response = "Estas horas são inválidas, favor inserir novamente."
       return JSONResponse(content={"erro": response}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    response = model.generate_content(
        f"crie um guia turístico curto porem detalhado para Belém do Pará durante o período de {req.hora_inicio} e {req.hora_fim}, "
        f"sendo estritamente importante levar em consideração essas preferências: {', '.join(req.preferencias)}, "
        "liste as atividades com sugestões clássicas de guias de turismo, como restaurantes sugeridos, atrações, celebrações e deslocamento."
    )
    return JSONResponse(content={"roteiro": response.text})