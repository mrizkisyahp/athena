from dataclasses import dataclass
from devtools.models import Agent

@dataclass(slots=True)
class ProviderRequest:
    agent: Agent
    instructions: str
    prompt: str

@dataclass(slots=True)
class ProviderResponse:
    output: str
    provider_name: str
    duration_seconds: float | None = None
