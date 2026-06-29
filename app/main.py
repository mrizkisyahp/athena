from fastapi import FastAPI

from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="Your personal Chief of Staff",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.app_name}"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }