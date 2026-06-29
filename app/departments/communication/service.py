from app.integrations.llm import LLMClient
from app.schemas.chat import ChatMessage, ChatRequest


class CommunicationDepartment:
    """
    Handles conversations with the user.
    """
    
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def chat(self, message: str) -> str:
        request = ChatRequest(
            messages = [
                ChatMessage(
                    role="user",
                    content=message,
                )
            ]
        )

        return await self.llm.generate(request)