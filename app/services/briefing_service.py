from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.responsibilities.service import ResponsibilityService
from app.schemas.chat import ChatRequest, ChatMessage


class BriefingService:
    """
    Generates Athena's daily briefing.
    """

    def __init__(
        self,
        responsibilities: ResponsibilityService,
        llm: LLMClient,
        prompts: PromptService,
    ):
        self._responsibilities = responsibilities
        self._llm = llm
        self._prompts = prompts

    async def generate_daily_briefing(self) -> str:
        today = self._responsibilities.get_due_today()
        high_priority = self._responsibilities.get_high_priority_today()
        overdue = self._responsibilities.get_overdue()
        completed = self._responsibilities.get_completed_today()

        context = f"""
High priority responsibilities today:
{self._format_tasks(high_priority)}

Today's responsibilities:
{self._format_tasks(today)}

Overdue responsibilities:
{self._format_tasks(overdue)}

Completed today:
{len(completed)} responsibility(ies)
"""
        
        user_prompt = f"""
Generate today's briefing.

{context}
"""

        request = ChatRequest(
            messages=[
                ChatMessage(
                    role="user",
                    content=user_prompt,
                )
            ]
        )

        return await self._llm.generate(request)

    def _format_tasks(self, tasks) -> str:
        if not tasks:
            return "None"
        
        return "\n".join(
            f"- {task.title} ({task.priority})"
            for task in tasks
        )
