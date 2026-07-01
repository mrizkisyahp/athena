from pathlib import Path
from devtools.models import Agent

class PromptLibrary:
    def __init__(self, prompts_dir: str = "devtools/prompts"):
        self.prompts_dir = Path(prompts_dir)
        
    def get_prompt(self, agent: Agent) -> str:
        prompt_filename = f"{agent.role.lower().replace(' ', '_')}.md"
        prompt_path = self.prompts_dir / prompt_filename
        if prompt_path.exists():
            return prompt_path.read_text()
        return f"You are a {agent.role}."
