from app.integrations.llm import LLMClient
from app.schemas.chat import ChatMessage, ChatRequest
from app.services.prompt_service import PromptService
from app.time.duration import Duration
from app.workload.service import WorkloadBalancer


class WorkloadService:
    def __init__(
        self,
        balancer: WorkloadBalancer,
        llm: LLMClient,
        prompts: PromptService,
    ):
        self._balancer = balancer
        self._llm = llm
        self._prompts = prompts

    async def analyze_workload(self, available_capacity: Duration) -> str:
        analysis = self._balancer.analyze(available_capacity)

        prompt_context = "Today's Workload\n\n"
        
        if analysis.total_workload is None:
            prompt_context += "Total Estimated Workload:\nUnknown\n\n"
        else:
            prompt_context += f"Total Estimated Workload:\n{analysis.total_workload}\n\n"
            
        prompt_context += f"Available Capacity:\n{analysis.available_capacity}\n\n"
        prompt_context += f"Overloaded:\n{'Yes' if analysis.overloaded else 'No'}\n\n"

        if analysis.suggested_deferrals:
            prompt_context += "Suggested Deferrals:\n"
            for task in analysis.suggested_deferrals:
                prompt_context += f"- {task.title}\n"
            prompt_context += "\n"
        else:
            if not analysis.overloaded:
                prompt_context += "Today's workload fits comfortably within the available capacity.\n\n"
            else:
                prompt_context += "Today's workload exceeds available capacity.\n"
                prompt_context += "No safe responsibilities can be deferred.\n\n"

        if analysis.reasoning:
            prompt_context += "Reasoning\n"
            for reason in analysis.reasoning:
                prompt_context += f"- {reason}\n"
            prompt_context += "\n"

        prompt_context += (
            "Explain this as Athena, the user's Personal Chief of Staff.\n"
            "Do not recommend deferring any responsibility other than those listed.\n"
            "Do not invent additional work.\n"
            "Encourage the user while being realistic."
        )

        request = ChatRequest(
            messages=[
                ChatMessage(role="user", content=prompt_context)
            ]
        )

        return await self._llm.generate(request)
