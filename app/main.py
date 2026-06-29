from fastapi import FastAPI

from app.config.settings import settings
from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.schemas.chat import ChatRequest

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

# Bootstrap Athena
llm = LLMClient()
communication = CommunicationDepartment(llm)
athena = AthenaKernel(communication)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with Athena.
    """
    user_message = request.messages[-1].content

    reply = await athena.chat(user_message)

    return {
        "reply": reply,
    }