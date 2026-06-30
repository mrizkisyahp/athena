from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.responsibilities.service import ResponsibilityService
from app.services.briefing_service import BriefingService
from app.services.prompt_service import PromptService
from app.advisors.availability import AvailabilityAdvisor
from app.advisors.router import QuestionRouter
from app.advisors.service import AdvisorService

class AthenaContainer:
    """
    Responsible for constructing Athena.
    """

    def __init__(self):
        self.llm = LLMClient()
        self.prompt_service = PromptService()

        self.communication = CommunicationDepartment(
            self.llm
        )

        self.responsibilities = ResponsibilityService()

        self.briefing = BriefingService(
            responsibilities=self.responsibilities,
            llm=self.llm,
            prompts=self.prompt_service,
        )

        self.availability_advisor = AvailabilityAdvisor(self.responsibilities)
        self.question_router = QuestionRouter([self.availability_advisor])
        self.advisor_service = AdvisorService(
            router=self.question_router,
            llm=self.llm,
            prompts=self.prompt_service,
        )

        self.kernel = AthenaKernel(
            self.communication,
            self.responsibilities
        )


container = AthenaContainer()