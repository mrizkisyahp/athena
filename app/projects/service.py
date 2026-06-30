from app.projects.models import Project
from app.responsibilities.service import ResponsibilityService
from app.responsibilities.models import Responsibility

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
