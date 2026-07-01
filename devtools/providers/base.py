from abc import ABC, abstractmethod
from devtools.providers.models import ProviderRequest, ProviderResponse

class BaseProvider(ABC):
    @abstractmethod
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        """Execute an agent request and return the provider's response."""
        pass
