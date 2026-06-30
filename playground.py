import asyncio
from datetime import timedelta
from app.planning.service import ExecutionPlanner
from app.planning.planning_service import PlanningService
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.services.time_service import TimeService
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService

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
    tomorrow = today + timedelta(days=1)

    r1 = Responsibility(title="Finish Sprint 7", priority=ResponsibilityPriority.CRITICAL, due_date=today)
    r2 = Responsibility(title="Review thesis", priority=ResponsibilityPriority.HIGH, due_date=tomorrow)

    service.add(r1)
    service.add(r2)

    planner = ExecutionPlanner(service)
    llm = LLMClient()
    prompts = PromptService()
    
    planning_service = PlanningService(planner, llm, prompts)
    response = await planning_service.generate_plan()
    
    print("Athena:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())