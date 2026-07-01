from devtools.models import Agent
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
    agent = Agent(name="TestAgent", role="Test Role", provider="Fake", model="fake-model")
    request = ProviderRequest(
        agent=agent,
        instructions="Say hello",
        prompt="You are a fake agent."
    )
    
    provider = FakeProvider()
    print("--- Provider Request ---")
    print(request)
    
    print("\n--- Provider Response ---")
    response = provider.execute(request)
    print(response)

if __name__ == "__main__":
    main()