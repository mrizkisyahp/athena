from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel
from app.responsibilities.service import ResponsibilityService


class AthenaContainer:
    """
    Responsible for constructing Athena.
    """

    def __init__(self):
        self.llm = LLMClient()

        self.communication = CommunicationDepartment(
            self.llm
        )

        self.responsibilities = ResponsibilityService()

        self.kernel = AthenaKernel(
            self.communication,
            self.responsibilities
        )


container = AthenaContainer()