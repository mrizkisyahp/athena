from app.projects.service import ProjectService
from app.responsibilities.models import Responsibility

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
    r1 = Responsibility(title="Sprint 6", project_id=athena.id)
    r2 = Responsibility(title="Advisor Framework", project_id=athena.id)
    r3 = Responsibility(title="PostgreSQL")
    
    responsibility_service.add(r1)
    responsibility_service.add(r2)
    responsibility_service.add(r3)
    
    print(f"Responsibilities for project {athena.name}:")
    for r in project_service.get_responsibilities(athena.id, responsibility_service):
        print(f"- {r.title}")

if __name__ == "__main__":
    main()