from typing import Final

from openai import AsyncOpenAI

from app.config.settings import settings
from app.schemas.chat import ChatRequest
from app.services.prompt_service import PromptService


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
        self.prompt_service = PromptService()

    async def generate(
        self,
        request: ChatRequest,
    ) -> str:
        system_prompt = self.prompt_service.load("system")

        response = await self.client.chat.completions.create(
            model=request.model or settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *[
                    message.model_dump()
                    for message in request.messages
                ],
            ],
        )

        if not response.choices:
            raise RuntimeError(f"LLM returned an invalid or empty response: {response}")

        return response.choices[0].message.content or ""
