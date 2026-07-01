import time
from openai import OpenAI
from devtools.providers.base import BaseProvider
from devtools.providers.models import ProviderRequest, ProviderResponse
from app.config.settings import settings

class NineRouterProviderError(Exception):
    """Exception raised for errors in the NineRouter provider."""
    pass

class NineRouterProvider(BaseProvider):
    def __init__(self):
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_base_url
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=request.agent.model,
                messages=[
                    {"role": "system", "content": request.prompt},
                    {"role": "user", "content": request.instructions}
                ]
            )
        except Exception as e:
            raise NineRouterProviderError(f"Provider execution failed: {str(e)}") from e
            
        duration = time.time() - start_time
        output = response.choices[0].message.content or ""
        
        return ProviderResponse(
            output=output,
            provider_name="NineRouter",
            duration_seconds=round(duration, 2)
        )
