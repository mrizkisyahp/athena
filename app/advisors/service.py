from app.advisors.router import QuestionRouter
from app.advisors.decision import AdvisorDecision, DecisionOutcome
from app.integrations.llm import LLMClient
from app.services.prompt_service import PromptService
from app.schemas.chat import ChatRequest, ChatMessage
from app.memory import MemoryRetriever, MemoryPromptBuilder

class AdvisorService:

    def __init__(
        self,
        router: QuestionRouter,
        llm: LLMClient,
        prompts: PromptService,
        memory_retriever: MemoryRetriever = None,
        insight_engine = None,
    ):
        self._router = router
        self._llm = llm
        self._prompts = prompts
        self._memory_retriever = memory_retriever
        self._insight_engine = insight_engine

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
        
        memory_context = ""
        if self._memory_retriever:
            relevant = self._memory_retriever.retrieve(question)
            memory_context = MemoryPromptBuilder.build(relevant)
            
        insight_context = ""
        if self._insight_engine:
            from app.awareness.constants import PLANNING_INSIGHT_CAPACITY
            from app.awareness.prompt import InsightPromptBuilder
            from app.services.time_service import TimeService
            
            day = TimeService.now().date()
            insights = self._insight_engine.generate(day, PLANNING_INSIGHT_CAPACITY)
            insight_context = InsightPromptBuilder.build(insights)
        
        prompt = (
            f"User Question:\n{question}\n\n"
            f"Decision:\n{decision.outcome.value}\n\n"
            f"Confidence:\n{decision.confidence}\n\n"
            f"Reasoning:\n{reasoning_list}\n"
            f"{memory_context}"
            f"{insight_context}"
            "Explain this decision as Athena, the user's Personal Chief of Staff.\n"
            "Be reassuring, practical, and concise."
        )

        request = ChatRequest(
            messages=[
                ChatMessage(role="user", content=prompt)
            ]
        )

        return await self._llm.generate(request)
