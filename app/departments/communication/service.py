class CommunicationDepartment:
    """
    Handles conversations with the user.
    """

    async def chat(self, message: str) -> str:
        raise NotImplementedError


communication = CommunicationDepartment()