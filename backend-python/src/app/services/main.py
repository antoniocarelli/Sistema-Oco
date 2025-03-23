from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_router

app = FastAPI(
    title="API do Modelo",
    description="API para o sistema Modelo",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(auth_router, prefix="/auth", tags=["autenticação"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Modelo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.services.main:app", host="0.0.0.0", port=8000, reload=True) 