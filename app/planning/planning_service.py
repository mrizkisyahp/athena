from app.planning.service import ExecutionPlanner
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.schemas.chat import ChatRequest, ChatMessage


class PlanningService:
    def __init__(
        self,
        planner: ExecutionPlanner,
        llm: LLMClient,
        prompts: PromptService,
    ):
        self._planner = planner
        self._llm = llm
        self._prompts = prompts

    async def generate_plan(self) -> str:
        plan = self._planner.generate_plan()

        if not plan.responsibilities:
            return "You have no outstanding responsibilities. Enjoy your free time!"

        tasks_text = []
        for i, r in enumerate(plan.responsibilities, 1):
            due_str = r.due_date.strftime("%Y-%m-%d %H:%M") if r.due_date else "None"
            tasks_text.append(f"{i}.\n{r.title}\nPriority:\n{r.priority.value.upper()}\nDue:\n{due_str}\n")

        tasks_joined = "\n".join(tasks_text)
        rationale_joined = "\n".join(f"- {reason}" for reason in plan.rationale)

        prompt = (
            f"Execution Plan\n\n"
            f"{tasks_joined}\n"
            f"Rationale\n\n"
            f"{rationale_joined}\n\n"
            f"Explain this plan as Athena, the user's Personal Chief of Staff.\n"
            f"Do not change the order.\n"
            f"Explain why the order makes sense.\n"
            f"Encourage execution."
        )

        request = ChatRequest(
            messages=[
                ChatMessage(role="user", content=prompt)
            ]
        )

        return await self._llm.generate(request)
