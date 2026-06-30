from fastapi import FastAPI, HTTPException

from app.config.settings import settings
from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.schemas.chat import ChatRequest
from app.bootstrap.container import container
from app.schemas.task import (
    CreateTaskRequest,
    TaskResponse,
)
from app.schemas.common import SuccessResponse
from app.schemas.mappers import to_task_response
from app.schemas.today import TodayResponse

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

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

    reply = await container.kernel.chat(user_message)

    return {
        "reply": reply,
    }

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest):

    responsibility = container.responsibilities.create(
        title=request.title,
        description=request.description,
        priority=request.priority,
        due_date=request.due_date,
    )

    return to_task_response(responsibility)

@app.get("/tasks", response_model=list[TaskResponse])
async def list_tasks():

    tasks = []

    for responsibility in container.responsibilities.get_all():

        tasks.append(to_task_response(responsibility))

    return tasks

@app.patch(
    "/tasks/{task_id}/complete",
    response_model=SuccessResponse,
)
async def complete_task(task_id: str):

    responsibility = container.responsibilities.complete(task_id)

    if responsibility is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return SuccessResponse(
        success=True,
        message="Task completed successfully.",
    )

@app.get(
    "/today",
    response_model=TodayResponse,
)
async def today():

    service = container.responsibilities

    return TodayResponse(
        today=[
            to_task_response(task)
            for task in service.get_due_today()
        ],
        overdue=[
            to_task_response(task)
            for task in service.get_overdue()
        ],
        completed_today=[
            to_task_response(task)
            for task in service.get_completed_today()
        ],
    )