from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.responsibilities.service import ResponsibilityService
from app.services.briefing_service import BriefingService
from app.services.prompt_service import PromptService


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

        self.kernel = AthenaKernel(
            self.communication,
            self.responsibilities
        )


container = AthenaContainer()