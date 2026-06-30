from app.advisors.router import QuestionRouter
from app.advisors.decision import AdvisorDecision, DecisionOutcome
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.schemas.chat import ChatRequest, ChatMessage

class AdvisorService:

    def __init__(
        self,
        router: QuestionRouter,
        llm: LLMClient,
        prompts: PromptService,
    ):
        self._router = router
        self._llm = llm
        self._prompts = prompts

    async def advise(self, question: str) -> str:
        advisor = self._router.route(question)
        
        if advisor:
            decision = advisor.advise(question)
        else:
            decision = AdvisorDecision(
                outcome=DecisionOutcome.CONDITIONAL,
                confidence=0.0,
                reasoning=[
                    "No advisor currently supports this question."
                ]
            )

        reasoning_list = "\n".join(f"- {reason}" for reason in decision.reasoning)
        
        prompt = (
            f"User Question:\n{question}\n\n"
            f"Decision:\n{decision.outcome.value}\n\n"
            f"Confidence:\n{decision.confidence}\n\n"
            f"Reasoning:\n{reasoning_list}\n\n"
            "Explain this decision as Athena, the user's Personal Chief of Staff.\n"
            "Be reassuring, practical, and concise."
        )

        request = ChatRequest(
            messages=[
                ChatMessage(role="user", content=prompt)
            ]
        )

        return await self._llm.generate(request)
