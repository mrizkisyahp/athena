from devtools.models import Agent, Task, AgentResult, PipelineRun, PipelineReport

def main():
    agent = Agent(name="Cohere North Mini Code", role="Executor", provider="Cohere", model="command-r")
    task = Task(title="DevTool #1", instructions="Implement domain model")
    result = AgentResult(agent=agent, output="Success", duration_seconds=1.5)
    run = PipelineRun(name="Sprint 10 PR 1", results=[result])
    report = PipelineReport(stage="Implementation", completed=True, summary="All models implemented.")

    print("--- Agent ---")
    print(agent)
    print("\n--- Task ---")
    print(task)
    print("\n--- AgentResult ---")
    print(result)
    print("\n--- PipelineRun ---")
    print(run)
    print("\n--- PipelineReport ---")
    print(report)

if __name__ == "__main__":
    main()