from app.projects.models import Project
from app.projects.progress import ProjectProgress
from app.responsibilities.service import ResponsibilityService
from app.responsibilities.models import Responsibility, ResponsibilityStatus

class ProjectService:
    """
    Manages the user's projects.
    """

    def __init__(self):
        self._projects: list[Project] = []

    def create(self, name: str, description: str = "") -> Project:
        normalized_name = name.lower()
        for p in self._projects:
            if p.name.lower() == normalized_name:
                raise ValueError(f"Project with name '{name}' already exists.")

        project = Project(
            name=name,
            description=description,
        )
        self._projects.append(project)
        return project

    def get_all(self) -> list[Project]:
        return self._projects.copy()

    def get_by_id(self, project_id: str) -> Project | None:
        for project in self._projects:
            if project.id == project_id:
                return project

        return None

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
