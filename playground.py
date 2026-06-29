import asyncio

from app.integrations.llm import LLMClient
from app.schemas.chat import ChatMessage, ChatRequest


async def main():

    llm = LLMClient()

    request = ChatRequest(
        messages=[
            ChatMessage(
                role="user",
                content="Reply with exactly: Athena is online.",
            )
        ]
    )

    response = await llm.generate(request)

    print(response)


asyncio.run(main())