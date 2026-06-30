import asyncio
from app.advisors.availability import AvailabilityAdvisor
from app.advisors.router import QuestionRouter
from app.advisors.service import AdvisorService
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.responsibilities.models import Responsibility, ResponsibilityPriority

class MockResponsibilityService:
    def __init__(self):
        self.due_today = [Responsibility(title="test", priority=ResponsibilityPriority.HIGH)]
        self.overdue = []

    def get_due_today(self):
        return self.due_today

    def get_overdue(self):
        return self.overdue

async def main():
    service = MockResponsibilityService()
    advisor = AvailabilityAdvisor(service)
    router = QuestionRouter([advisor])
    llm = LLMClient()
    prompts = PromptService()
    
    advisor_service = AdvisorService(router, llm, prompts)
    
    q = "Can I game tonight?"
    print(f"User: {q}\n")
    
    response = await advisor_service.advise(q)
    print(f"Athena:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())