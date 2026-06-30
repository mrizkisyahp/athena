import asyncio
from datetime import timedelta
from app.services.time_service import TimeService
from app.responsibilities.models import Responsibility, ResponsibilityPriority, ResponsibilityStatus
from app.responsibilities.service import ResponsibilityService
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.services.briefing_service import BriefingService

async def main():
    service = ResponsibilityService()
    now = TimeService.now()

    # Overdue
    service.add(
        Responsibility(
            title="Thesis proposal",
            priority=ResponsibilityPriority.MEDIUM,
            due_date=now - timedelta(days=1),
        )
    )

    # Due today
    service.add(
        Responsibility(
            title="Upload employee report",
            priority=ResponsibilityPriority.HIGH,
            due_date=now,
        )
    )

    # Completed today
    completed = Responsibility(
        title="Check emails",
        status=ResponsibilityStatus.COMPLETED,
        completed_at=now,
    )
    service.add(completed)

    llm = LLMClient()
    prompts = PromptService()

    briefing_service = BriefingService(
        responsibilities=service,
        llm=llm,
        prompts=prompts,
    )

    response = await briefing_service.generate_daily_briefing()
    print(response)

if __name__ == "__main__":
    asyncio.run(main())