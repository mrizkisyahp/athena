from typing import Final

from openai import AsyncOpenAI

from app.config.settings import settings
from app.schemas.chat import ChatRequest
from app.services.prompt_service import PromptService
from app.logging.logger import logger


class LLMClient:
    """
    Generic LLM client.

    Athena never talks directly to a specific provider.
    Athena talks to this abstraction.

    It works with any OpenAI-compatible API (e.g. NVIDIA NIM, OpenRouter).
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
            max_tokens=8192,
        )

        if not response.choices:
            raise RuntimeError(f"LLM returned an invalid or empty response: {response}")

        logger.info(
            "LLM request completed",
            model=request.model or settings.llm_model,
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
        )

        return response.choices[0].message.content or ""