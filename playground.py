from pathlib import Path
from devtools.config import EngineeringTeam, Profiles
from devtools.providers.nine_router import NineRouterProvider
from devtools.providers.models import ProviderRequest

def main():
    agents = EngineeringTeam.get_all_agents()
    provider = NineRouterProvider()
    
    for agent in agents:
        profile = Profiles.ACTIVE_MAPPING[agent]
        if profile.provider_type == "fake":
            continue
            
        prompt_path = Path(f"devtools/prompts/{agent.role.lower().replace(' ', '_')}.md")
        prompt_content = prompt_path.read_text() if prompt_path.exists() else f"You are a {agent.role}."
        
        request = ProviderRequest(
            agent=agent,
            profile=profile,
            instructions="Say hello briefly.",
            prompt=prompt_content
        )
        
        print(f"\n--- NineRouter Request: {agent.role} ---")
        print(f"Agent: {agent.name}")
        print(f"Profile: {profile.name} (Model: {profile.model})")
        
        try:
            response = provider.execute(request)
            print(f"--- NineRouter Response: {agent.role} ---")
            print(f"Provider: {response.provider_name}")
            print(f"Duration: {response.duration_seconds}s")
            print(f"Output:\n{response.output}")
        except Exception as e:
            print(f"FAILED: {str(e)}")

if __name__ == "__main__":
    main()