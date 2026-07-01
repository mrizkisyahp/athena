import time
from openai import OpenAI
from devtools.providers.base import BaseProvider
from devtools.providers.models import ProviderRequest, ProviderResponse
from app.config.settings import settings

class NineRouterProviderError(Exception):
    """Exception raised for errors in the NineRouter provider."""
    pass

class NineRouterProvider(BaseProvider):
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        start_time = time.time()
        profile = request.profile
        
        # Safely resolve API key from settings
        api_key = getattr(settings, profile.api_key_source, None) if profile.api_key_source else None
        
        if not api_key:
            raise NineRouterProviderError(f"Missing API key for source: {profile.api_key_source}")
            
        client = OpenAI(
            api_key=api_key,
            base_url=profile.base_url
        )
        
        try:
            response = client.chat.completions.create(
                model=profile.model,
                messages=[
                    {"role": "system", "content": request.prompt},
                    {"role": "user", "content": request.instructions}
                ]
            )
        except Exception as e:
            raise NineRouterProviderError(f"NineRouter execution failed: {str(e)}") from e
            
        duration = time.time() - start_time
        output = response.choices[0].message.content or ""
        
        return ProviderResponse(
            output=output,
            provider_name="NineRouter",
            duration_seconds=round(duration, 2)
        )
