from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.responsibilities.service import ResponsibilityService
from app.services.briefing_service import BriefingService
from app.services.prompt_service import PromptService
from app.advisors.availability import AvailabilityAdvisor
from app.advisors.router import QuestionRouter
from app.advisors.service import AdvisorService

from app.memory.service import MemoryService
from app.memory.retrieval import MemoryRetriever

from app.projects.service import ProjectService
from app.calendar.service import EventService
from app.planning.service import ExecutionPlanner
from app.planning.planning_service import PlanningService

class AthenaContainer:
    """
    Central dependency injection container.
    """

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_service = PromptService()

        self.communication = CommunicationDepartment(
            self.llm
        )

        self.responsibilities = ResponsibilityService()
        self.projects = ProjectService()
        self.memories = MemoryService()
        self.events = EventService()
        self.memory_retriever = MemoryRetriever(self.memories)
        self.planner = ExecutionPlanner(self.responsibilities)

        self.briefing = BriefingService(
            responsibilities=self.responsibilities,
            llm=self.llm,
            prompts=self.prompt_service,
            memory_retriever=self.memory_retriever,
        )

        self.planning_service = PlanningService(
            planner=self.planner,
            llm=self.llm,
            prompts=self.prompt_service,
            memory_retriever=self.memory_retriever,
        )

        self.availability_advisor = AvailabilityAdvisor(self.responsibilities)
        from app.advisors.capacity import CapacityAdvisor
        self.capacity_advisor = CapacityAdvisor(self.planner)
        
        self.question_router = QuestionRouter([
            self.availability_advisor,
            self.capacity_advisor
        ])
        
        self.advisor_service = AdvisorService(
            router=self.question_router,
            llm=self.llm,
            prompts=self.prompt_service,
            memory_retriever=self.memory_retriever,
        )

        self.kernel = AthenaKernel(
            self.communication,
            self.responsibilities
        )
        
        from app.workload.service import WorkloadBalancer
        from app.workload.workload_service import WorkloadService
        
        self.workload_balancer = WorkloadBalancer(self.planner)
        self.workload_service = WorkloadService(
            balancer=self.workload_balancer,
            llm=self.llm,
            prompts=self.prompt_service,
        )


container = AthenaContainer()