from fastapi import FastAPI
from starlette.responses import HTMLResponse, FileResponse

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='WikiBel - Repertório de Belém')
app.include_router(api_router, prefix=settings.API_V1_SRT)

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse('templates/menu.html')

@app.get("/api/v1/members/login", response_class=HTMLResponse)
async def login_screen():
    return FileResponse('templates/login.html')
@app.get("/api/v1/members/signup", response_class=HTMLResponse)
async def signup_screen():
    return FileResponse('templates/signup.html')
@app.get("/api/v1/members/account", response_class=HTMLResponse)
async def account_screen():
    return FileResponse('templates/account.html')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                     log_level="info", reload=True)