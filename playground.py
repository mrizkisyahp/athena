from devtools.models import Agent, Task, AgentResult, PipelineRun, PipelineReport
from devtools.config import EngineeringTeam
from pathlib import Path

def main():
    print("--- Prompt Library Validation ---")
    prompt_dir = Path("devtools/prompts")
    for prompt_file in prompt_dir.glob("*.md"):
        print(f"\n[{prompt_file.name}]")
        print("-" * 40)
        print(prompt_file.read_text())
        print("-" * 40)

if __name__ == "__main__":
    main()