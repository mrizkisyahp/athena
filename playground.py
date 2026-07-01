import sys
from devtools.models import PipelineRequest
from devtools.engine import PipelineEngine
from devtools.providers.nine_router import NineRouterProvider
from devtools.runtime import ExecutionRuntime
from devtools.history import RunHistory
from devtools.orchestrator import PipelineOrchestrator

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Setup Infrastructure
    engine = PipelineEngine()
    provider = NineRouterProvider()
    runtime = ExecutionRuntime(provider=provider)
    history = RunHistory()
    
    orchestrator = PipelineOrchestrator(
        engine=engine, 
        runtime=runtime, 
        history=history
    )
    
    # Execute Workflow
    print("Starting Orchestrator Workflow...")
    request = PipelineRequest(title="Sprint 10 PR1", touches_database=False)
    run = orchestrator.execute_pipeline(request, instructions="Say hello briefly!")
    
    # Print Report
    print("\n--- Pipeline Complete ---")
    print(f"Stages Executed: {len(run.results)} / {len(run.planned_agents)}")
    total_duration = sum(r.duration_seconds for r in run.results if r.duration_seconds)
    print(f"Duration: {total_duration:.2f}s")
    status = "PASS" if run.report.completed else "FAIL"
    print(f"Status: {status}")
    print(f"Summary: {run.report.summary}")

if __name__ == "__main__":
    main()