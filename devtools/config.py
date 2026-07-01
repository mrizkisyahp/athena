from devtools.models import Agent

class EngineeringTeam:
    TECHNICAL_LEAD = Agent(
        name="ChatGPT",
        role="Technical Lead",
        provider="OpenAI",
        model="gpt-4",
        is_conditional=False
    )
    
    DEVELOPMENT_ORCHESTRATOR = Agent(
        name="Antigravity",
        role="Development Orchestrator",
        provider="Google DeepMind",
        model="antigravity",
        is_conditional=False
    )
    
    ARCHITECT = Agent(
        name="Kimi K2.6",
        role="Architect",
        provider="Moonshot",
        model="moonshot-v1",
        is_conditional=False
    )
    
    BACKEND_EXECUTOR = Agent(
        name="Cohere North Mini Code",
        role="Backend Executor",
        provider="Cohere",
        model="command-r",
        is_conditional=False
    )
    
    DATABASE_REVIEWER = Agent(
        name="Llama 3.3 70B",
        role="Database Reviewer",
        provider="Meta",
        model="llama-3.3-70b-instruct",
        is_conditional=True
    )
    
    QA_REVIEWER = Agent(
        name="gpt-oss-120B",
        role="QA Reviewer",
        provider="OpenAI",
        model="gpt-oss-120b",
        is_conditional=False
    )
    
    @classmethod
    def get_all_agents(cls) -> list[Agent]:
        return [
            cls.TECHNICAL_LEAD,
            cls.DEVELOPMENT_ORCHESTRATOR,
            cls.ARCHITECT,
            cls.BACKEND_EXECUTOR,
            cls.DATABASE_REVIEWER,
            cls.QA_REVIEWER
        ]
