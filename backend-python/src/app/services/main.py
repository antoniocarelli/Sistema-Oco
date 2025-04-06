from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_router
import logging
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from app.core.init_db import init_db

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inicializa o banco de dados
init_db()

app = FastAPI(
    title="API do Modelo",
    description="API para o sistema Modelo",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost:4200",      # Frontend local
    "http://127.0.0.1:4200",     # Frontend local
    "http://frontend:4200",       # Frontend no Docker
    "http://localhost:8000",      # Backend local
    "http://127.0.0.1:8000",     # Backend local
    "http://backend:8000",        # Backend no Docker
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

# Middleware para log de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Recebida requisição: {request.method} {request.url}")
    logger.debug(f"Headers: {request.headers}")
    logger.debug(f"Origin: {request.headers.get('origin')}")
    
    response = await call_next(request)
    
    # Adiciona headers CORS manualmente
    origin = request.headers.get("origin")
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    
    logger.debug(f"Resposta enviada: {response.status_code}")
    logger.debug(f"Headers da resposta: {response.headers}")
    return response

# Rota de teste CORS
@app.options("/auth/login")
async def options_login(request: Request):
    origin = request.headers.get("origin")
    headers = {
        "Access-Control-Allow-Origin": origin if origin in origins else "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "3600"
    }
    return JSONResponse(status_code=200, headers=headers)

# Inclusão das rotas
app.include_router(auth_router, prefix="/auth", tags=["autenticação"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Modelo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.services.main:app", host="0.0.0.0", port=8000, reload=True) 