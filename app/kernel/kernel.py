from app.departments.communication.service import CommunicationDepartment
from app.logging.logger import logger
from app.responsibilities.service import ResponsibilityService


class AthenaKernel:
    """
    Central coordinator for Athena

    The Kernel never performs business logic
    It only coordinates departments
    """

    def __init__(
        self,
        communication: CommunicationDepartment,
        responsibilities: ResponsibilityService,
    ):
        self.communication = communication
        self.responsibilities = responsibilities

    async def chat(self, message: str) -> str:
        logger.info(
            "Kernel received chat request",
            message_length=len(message),
        )
        
        return await self.communication.chat(message)