from devtools.models import Agent
from devtools.providers.models import ProviderProfile

class EngineeringTeam:
    TECHNICAL_LEAD = Agent(
        name="ChatGPT",
        role="Technical Lead",
        is_conditional=False
    )
    
    DEVELOPMENT_ORCHESTRATOR = Agent(
        name="Antigravity",
        role="Development Orchestrator",
        is_conditional=False
    )
    
    ARCHITECT = Agent(
        name="Kimi K2.6",
        role="Architect",
        is_conditional=False
    )
    
    BACKEND_EXECUTOR = Agent(
        name="Cohere North Mini Code",
        role="Backend Executor",
        is_conditional=False
    )
    
    DATABASE_REVIEWER = Agent(
        name="Llama 3.3 70B",
        role="Database Reviewer",
        is_conditional=True
    )
    
    QA_REVIEWER = Agent(
        name="gpt-oss-120B",
        role="QA Reviewer",
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

class Profiles:
    FAKE = ProviderProfile(
        name="Fake Profile",
        provider_type="fake",
        base_url=None,
        model="fake-model",
        api_key_source=None
    )
    
    ACTIVE_MAPPING = {
        EngineeringTeam.TECHNICAL_LEAD: FAKE,
        EngineeringTeam.DEVELOPMENT_ORCHESTRATOR: FAKE,
        EngineeringTeam.ARCHITECT: FAKE,
        EngineeringTeam.BACKEND_EXECUTOR: FAKE,
        EngineeringTeam.DATABASE_REVIEWER: FAKE,
        EngineeringTeam.QA_REVIEWER: FAKE,
    }
