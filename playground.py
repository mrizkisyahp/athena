import asyncio
from datetime import timedelta
from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.services.time_service import TimeService

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

async def main():
    service = MockResponsibilityService()
    now = TimeService.now()
    today = now.replace(hour=23, minute=59, second=59)

    r1 = Responsibility(title="Sprint 7", project_id="Athena", priority=ResponsibilityPriority.MEDIUM, due_date=today)
    r2 = Responsibility(title="Review Paper", project_id="Thesis", priority=ResponsibilityPriority.MEDIUM, due_date=today)
    r3 = Responsibility(title="Write Docs", project_id="Athena", priority=ResponsibilityPriority.MEDIUM, due_date=today)
    r4 = Responsibility(title="Fix API", project_id="Athena", priority=ResponsibilityPriority.MEDIUM, due_date=today)

    r1.created_at = now - timedelta(minutes=4)
    r2.created_at = now - timedelta(minutes=3)
    r3.created_at = now - timedelta(minutes=2)
    r4.created_at = now - timedelta(minutes=1)

    service.add(r1)
    service.add(r2)
    service.add(r3)
    service.add(r4)

    planner = ExecutionPlanner(service)
    plan = planner.generate_plan()
    
    for r in plan.responsibilities:
        print(f"{r.title}")

if __name__ == "__main__":
    asyncio.run(main())