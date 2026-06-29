from typing import Final

from openai import AsyncOpenAI

from app.config.settings import settings
from app.schemas.chat import ChatRequest


class LLMClient:
    """
    Generic LLM client.

    Athena never talks directly to OpenRouter.
    Athena talks to this abstraction.

    Current provider:
        OpenRouter

    Future providers:
        - OpenAI
        - Anthropic
        - Local LLM
        - Other OpenAI-compatible APIs
    """


    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    async def generate(
        self,
        request: ChatRequest,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=request.model or settings.llm_model,
            messages=[
                message.model_dump()
                for message in request.messages
            ],
        )

        if not response.choices:
            raise RuntimeError(f"LLM returned an invalid or empty response: {response}")

        return response.choices[0].message.content or ""
