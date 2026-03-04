from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine
from .routers import recursos, ia
from loguru import logger
import sys

# logs
logger.remove() 
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)
logger.add(
    "logs/api.log",
    rotation="500 MB",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)
# Criar tabelas no banco
from .models import SQLModel
SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para Hub Inteligente de Recursos Educacionais",
    version="1.0.0",
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#endpoints
app.include_router(recursos.router)
app.include_router(ia.router)

@app.get("/")
async def root():
    return {
        "message": "🚀 Hubify API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "ai_configured": bool(settings.GEMINI_API_KEY)
    }


@app.on_event("startup")
async def startup_event():
    logger.info("API iniciada com sucesso!")
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY não configurada. Usando modo simulação para IA.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API encerrada.")