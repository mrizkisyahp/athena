from devtools.models import PipelineRun, PipelineReport
from devtools.history import RunHistory

def main():
    history = RunHistory()
    
    run1 = PipelineRun(name="Sprint 10 PR1", report=PipelineReport(stage="Done", completed=True, summary="First PR done"))
    run2 = PipelineRun(name="Sprint 10 PR2", report=PipelineReport(stage="Done", completed=True, summary="Second PR done"))
    
    history.add(run1)
    history.add(run2)
    
    print("--- Stored Runs ---")
    for r in history.get_all():
        print(r.name)
        
    print("\n--- Retrieve Run ---")
    retrieved = history.get("Sprint 10 PR1")
    if retrieved:
        print(f"Found: {retrieved.name} - {retrieved.report.summary if retrieved.report else 'No report'}")
    else:
        print("Run not found")

if __name__ == "__main__":
    main()