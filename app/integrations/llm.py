class LLMClient:
    """
    Abstract LLM Client.

    Current Provider:
        9router
        Omnirouter (potentially)
    """

    async def generate(self, message: str) -> str:
        raise NotImplementedError


llm = LLMClient()