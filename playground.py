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

    # LOW
    service.add(
        Responsibility(
            title="Buy milk",
            priority=ResponsibilityPriority.LOW,
            due_date=now,
        )
    )

    # HIGH
    service.add(
        Responsibility(
            title="Employee report",
            priority=ResponsibilityPriority.HIGH,
            due_date=now,
        )
    )

    # CRITICAL
    service.add(
        Responsibility(
            title="Final thesis submission",
            priority=ResponsibilityPriority.CRITICAL,
            due_date=now,
        )
    )

    llm = LLMClient()
    prompts = PromptService()

    briefing_service = BriefingService(
        responsibilities=service,
        llm=llm,
        prompts=prompts,
    )

    response = await briefing_service.generate_daily_briefing()
    
    # Encode and decode to avoid Windows cp1252 print errors with emojis
    print(response.encode("utf-8", "replace").decode("utf-8", "replace"))

if __name__ == "__main__":
    asyncio.run(main())