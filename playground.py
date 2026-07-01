from pathlib import Path
from devtools.config import EngineeringTeam, Profiles
from devtools.providers.base import BaseProvider
from devtools.providers.models import ProviderRequest, ProviderResponse

class FakeProvider(BaseProvider):
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            output="Hello from Fake Provider",
            provider_name="FakeProvider",
            duration_seconds=0.1
        )

def main():
    agent = EngineeringTeam.ARCHITECT
    profile = Profiles.ACTIVE_MAPPING[agent]
    prompt_path = Path("devtools/prompts/architect.md")
    prompt_content = prompt_path.read_text() if prompt_path.exists() else "You are an architect."
    
    request = ProviderRequest(
        agent=agent,
        profile=profile,
        instructions="Say hello",
        prompt=prompt_content
    )
    
    print("--- Fake Request ---")
    print(f"Agent: {agent.name}")
    print(f"Profile: {profile.name} (Model: {profile.model})")
    
    provider = FakeProvider()
    response = provider.execute(request)
    
    print("\n--- Fake Response ---")
    print(f"Provider: {response.provider_name}")
    print(f"Duration: {response.duration_seconds}s")
    print(f"Output:\n{response.output}")

if __name__ == "__main__":
    main()