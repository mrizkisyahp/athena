from app.projects.service import ProjectService
from app.responsibilities.models import Responsibility, ResponsibilityStatus

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def main():
    project_service = ProjectService()
    responsibility_service = MockResponsibilityService()
    
    # Create project Athena
    athena = project_service.create("Athena")
    
    # Create Responsibilities
    r1 = Responsibility(title="Sprint 5", project_id=athena.id, status=ResponsibilityStatus.COMPLETED)
    r2 = Responsibility(title="Sprint 6", project_id=athena.id, status=ResponsibilityStatus.COMPLETED)
    r3 = Responsibility(title="Sprint 7", project_id=athena.id, status=ResponsibilityStatus.IN_PROGRESS)
    r4 = Responsibility(title="Sprint 8", project_id=athena.id, status=ResponsibilityStatus.TODO)
    
    responsibility_service.add(r1)
    responsibility_service.add(r2)
    responsibility_service.add(r3)
    responsibility_service.add(r4)
    
    progress = project_service.get_progress(athena.id, responsibility_service)
    print("Project Progress")
    print(f"Total: {progress.total}")
    print(f"Completed: {progress.completed}")
    print(f"Remaining: {progress.remaining}")
    print(f"Progress: {progress.percentage}%")

if __name__ == "__main__":
    main()