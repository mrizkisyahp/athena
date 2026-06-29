from app.departments.communication.service import CommunicationDepartment


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
        return await self.communication.chat(message)