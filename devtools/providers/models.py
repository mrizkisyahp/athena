from dataclasses import dataclass
from devtools.models import Agent

@dataclass(slots=True)
class ProviderProfile:
    name: str
    provider_type: str
    base_url: str | None
    model: str
    api_key_source: str | None

@dataclass(slots=True)
class ProviderRequest:
    agent: Agent
    profile: ProviderProfile
    instructions: str
    prompt: str

@dataclass(slots=True)
class ProviderResponse:
    output: str
    provider_name: str
    duration_seconds: float | None = None
