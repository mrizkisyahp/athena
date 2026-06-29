from fastapi import FastAPI

app = FastAPI(
    title="Athena",
    description="Your personal Chief of Staff",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to Athena"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "athena",
    }