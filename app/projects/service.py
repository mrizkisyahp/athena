from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.projects.models import Project
from app.projects.progress import ProjectProgress
from app.responsibilities.service import ResponsibilityService
from app.responsibilities.models import Responsibility, ResponsibilityStatus
from app.database.session import SessionLocal
from app.database.mappers import to_project_domain, to_project_orm
from app.database.models import ProjectORM

class ProjectService:
    """
    Manages the user's projects.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def create(self, name: str, description: str = "") -> Project:
        project = Project(
            name=name,
            description=description,
        )
        
        orm_model = to_project_orm(project)

        with self._session_factory() as session:
            try:
                session.add(orm_model)
                session.commit()
            except IntegrityError:
                session.rollback()
                raise ValueError(f"Project with name '{name}' already exists.")

        return project

    def get_all(self) -> list[Project]:
        with self._session_factory() as session:
            models = session.scalars(select(ProjectORM)).all()
            return [to_project_domain(model) for model in models]

    def get_by_id(self, project_id: str) -> Project | None:
        with self._session_factory() as session:
            model = session.get(ProjectORM, project_id)
            if not model:
                return None
            return to_project_domain(model)

    def get_responsibilities(
        self,
        project_id: str,
        responsibility_service: ResponsibilityService,
    ) -> list[Responsibility]:
        return [
            responsibility
            for responsibility in responsibility_service.get_all()
            if responsibility.project_id == project_id
        ]

    def get_progress(
        self,
        project_id: str,
        responsibility_service: ResponsibilityService,
    ) -> ProjectProgress:
        responsibilities = self.get_responsibilities(project_id, responsibility_service)
        
        total = len(responsibilities)
        if total == 0:
            return ProjectProgress(
                total=0,
                completed=0,
                remaining=0,
                percentage=0.0
            )
            
        completed = sum(
            1 for r in responsibilities 
            if r.status == ResponsibilityStatus.COMPLETED
        )
        remaining = total - completed
        percentage = (completed / total) * 100.0
        
        return ProjectProgress(
            total=total,
            completed=completed,
            remaining=remaining,
            percentage=percentage
        )
