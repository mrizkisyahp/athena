from app.departments.communication.service import CommunicationDepartment
from app.logging.logger import logger


class AthenaKernel:
    """
    Central coordinator for Athena

    The Kernel never performs business logic
    It only coordinates departments
    """

    def __init__(
        self,
        communication: CommunicationDepartment,
    ):
        self.communication = communication

    async def chat(self, message: str) -> str:
        logger.info(
            "Kernel received chat request",
            message_length=len(message),
        )
        
        return await self.communication.chat(message)