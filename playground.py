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
    print("Starting Orchestrator Workflow for Sprint 10 PR 1...")
    request = PipelineRequest(title="Sprint 10 PR1: Memory Domain Model", touches_database=False)
    
    instructions = """
Target Project: Athena
Sprint: 10
PR: #1
Feature: Memory Domain Model

Objective: Create the foundational domain objects for Athena's long-term memory system.

Requirements:
Create `app/memory/__init__.py` and `app/memory/models.py`.

Implement:
1. `Memory`: A domain dataclass representing a single long-lived fact.
   Suggested fields: id, memory_type, content, importance, created_at
   Use the existing TimeService for timestamps and UUIDs consistent with the rest of Athena.
2. `MemoryType` (Enum): PREFERENCE, GOAL, ROUTINE, CONTEXT
3. `MemoryImportance` (Enum): LOW, MEDIUM, HIGH

Constraints:
- No database.
- No HTTP endpoints.
- No service layer.
- No LLM integration.
- Pure domain only.
- Match the style of existing domain models throughout Athena.

Playground:
Instantiate several memories and verify construction.
Example:
Preference: "I prefer coding after dinner."
Goal: "Graduate this year."
Routine: "Review tasks every morning."
Print the resulting dataclasses.
"""
    
    run = orchestrator.execute_pipeline(request, instructions=instructions)
    
    # Save Pipeline Results to a file so Antigravity can read it easily
    with open("pipeline_report.md", "w", encoding="utf-8") as f:
        f.write(f"--- Pipeline Complete ---\n")
        f.write(f"Stages Executed: {len(run.results)} / {len(run.planned_agents)}\n")
        total_duration = sum(r.duration_seconds for r in run.results if r.duration_seconds)
        f.write(f"Duration: {total_duration:.2f}s\n")
        status = "PASS" if run.report.completed else "FAIL"
        f.write(f"Status: {status}\n")
        f.write(f"Summary: {run.report.summary}\n\n")
        for result in run.results:
            f.write(f"[{result.agent.role}]\n")
            f.write(f"{result.output.strip()}\n\n")
            
    print("Pipeline output saved to pipeline_report.md")

if __name__ == "__main__":
    main()