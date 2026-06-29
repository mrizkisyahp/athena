from app.departments.communication.service import CommunicationDepartment
from app.integrations.llm import LLMClient
from app.kernel.kernel import AthenaKernel


class AthenaContainer:
    """
    Responsible for constructing Athena.
    """

    def __init__(self):
        self.llm = LLMClient()

        self.communication = CommunicationDepartment(
            self.llm
        )

        self.kernel = AthenaKernel(
            self.communication
        )


container = AthenaContainer()