from devtools.models import Agent
from devtools.providers.models import ProviderProfile
from app.config.settings import settings

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
    NINE_ROUTER_ARCHITECT = ProviderProfile(
        name="9router - Architect",
        provider_type="nine_router",
        base_url=settings.devtools_ninerouter_base_url,
        model=settings.devtools_architect_model,
        api_key_source="devtools_ninerouter_api_key"
    )
    
    NINE_ROUTER_BACKEND_EXECUTOR = ProviderProfile(
        name="9router - Backend Executor",
        provider_type="nine_router",
        base_url=settings.devtools_ninerouter_base_url,
        model=settings.devtools_backend_executor_model,
        api_key_source="devtools_ninerouter_api_key"
    )
    
    NINE_ROUTER_DATABASE_REVIEWER = ProviderProfile(
        name="9router - Database Reviewer",
        provider_type="nine_router",
        base_url=settings.devtools_ninerouter_base_url,
        model=settings.devtools_database_reviewer_model,
        api_key_source="devtools_ninerouter_api_key"
    )
    
    NINE_ROUTER_QA_REVIEWER = ProviderProfile(
        name="9router - QA Reviewer",
        provider_type="nine_router",
        base_url=settings.devtools_ninerouter_base_url,
        model=settings.devtools_qa_reviewer_model,
        api_key_source="devtools_ninerouter_api_key"
    )
    ACTIVE_MAPPING = {
        EngineeringTeam.TECHNICAL_LEAD: FAKE,
        EngineeringTeam.DEVELOPMENT_ORCHESTRATOR: FAKE,
        EngineeringTeam.ARCHITECT: NINE_ROUTER_ARCHITECT,
        EngineeringTeam.BACKEND_EXECUTOR: NINE_ROUTER_BACKEND_EXECUTOR,
        EngineeringTeam.DATABASE_REVIEWER: NINE_ROUTER_DATABASE_REVIEWER,
        EngineeringTeam.QA_REVIEWER: NINE_ROUTER_QA_REVIEWER,
    }
