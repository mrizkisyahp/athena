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
from app.time.duration import Duration

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
    duration = None
    if request.estimated_duration_minutes is not None:
        try:
            duration = Duration(request.estimated_duration_minutes)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    task = container.responsibilities.create(
        title=request.title,
        description=request.description,
        priority=request.priority,
        due_date=request.due_date,
        project_id=request.project_id,
        estimated_duration=duration,
    )

    return to_task_response(task)

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

@app.get("/daily-briefing")
async def daily_briefing():
    return {
        "briefing": await container.briefing.generate_daily_briefing()
    }

from app.schemas.advisor import AdvisorRequest, AdvisorResponse

@app.post(
    "/advisor",
    response_model=AdvisorResponse,
)
async def advisor(
    request: AdvisorRequest,
):
    answer = await container.advisor_service.advise(
        request.question
    )

    return AdvisorResponse(
        answer=answer
    )

from app.schemas.project import (
    ProjectRequest,
    ProjectResponse,
    ProjectOverviewResponse,
    ProjectProgressResponse
)

@app.post("/projects", response_model=ProjectResponse)
async def create_project(request: ProjectRequest):
    try:
        project = container.projects.create(
            name=request.name,
            description=request.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
    )

@app.get("/projects", response_model=list[ProjectResponse])
async def list_projects():
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            created_at=p.created_at,
        )
        for p in container.projects.get_all()
    ]

@app.get("/projects/{project_id}", response_model=ProjectOverviewResponse)
async def get_project(project_id: str):
    project = container.projects.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
        
    progress = container.projects.get_progress(project_id, container.responsibilities)
    responsibilities = container.projects.get_responsibilities(project_id, container.responsibilities)
    
    return ProjectOverviewResponse(
        project=ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
        ),
        progress=ProjectProgressResponse(
            total=progress.total,
            completed=progress.completed,
            remaining=progress.remaining,
            percentage=progress.percentage,
        ),
        responsibilities=[
            to_task_response(r) for r in responsibilities
        ]
    )

from app.schemas.planning import ExecutionPlanResponse

@app.get(
    "/execution-plan",
    response_model=ExecutionPlanResponse,
)
async def execution_plan():
    plan = await container.planning_service.generate_plan()

    return ExecutionPlanResponse(
        plan=plan
    )