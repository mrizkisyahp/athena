from typing import Final

from openai import AsyncOpenAI

from app.config.settings import settings


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


    def __init__(self) -> None:
        self._client: Final = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    async def generate(
        self,
        prompt: str,
        *,
        model: str | None = None,
    ) -> str:
        """
        Generate a response from the configured LLM.
        """

        response = await self._client.chat.completions.create(
            model=model or settings.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("LLM returned an empty response.")

        return content


llm_client = LLMClient()