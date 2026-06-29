from app.integrations.llm import LLMClient
from app.schemas.chat import ChatMessage, ChatRequest
from app.logging.logger import logger


class CommunicationDepartment:
    """
    Handles conversations with the user.
    """
    
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def chat(self, message: str) -> str:
        logger.info(
            "Communication Department received chat request",
            message_length=len(message),
        )
        request = ChatRequest(
            messages = [
                ChatMessage(
                    role="user",
                    content=message,
                )
            ]
        )

        reply = await self.llm.generate(request)

        logger.info(
            "Athena generated reply",
            reply_length=len(reply),
        )

        return reply