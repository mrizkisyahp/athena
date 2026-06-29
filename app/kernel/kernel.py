class AthenaKernel:
    """
    Central coordinator for Athena

    The Kernel never performs business logic
    It only coordinates departments
    """

    async def chat(self, message: str) -> str:
        raise NotImplementedError


kernel = AthenaKernel()