from devtools.models import Agent, Task, AgentResult, PipelineRun, PipelineReport
from devtools.config import EngineeringTeam

def main():
    print("--- Pipeline Configuration Loaded ---")
    for agent in EngineeringTeam.get_all_agents():
        status = "Conditional" if agent.is_conditional else "Always Active"
        print(f"[{agent.role}] {agent.name} (Model: {agent.model}) - {status}")
        
    print("\n--- Validating Run Construction ---")
    task = Task(title="DevTool #2", instructions="Implement pipeline config")
    executor = EngineeringTeam.BACKEND_EXECUTOR
    result = AgentResult(agent=executor, output="Config implemented.", duration_seconds=1.2)
    run = PipelineRun(name="Sprint 10 PR 2", results=[result])
    report = PipelineReport(stage="Configuration", completed=True, summary="Agents loaded successfully.")
    
    print(run)
    print(report)

if __name__ == "__main__":
    main()