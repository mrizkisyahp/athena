import sys
from devtools.engine import PipelineEngine
from devtools.models import PipelineRequest
from devtools.providers.nine_router import NineRouterProvider
from devtools.runtime import ExecutionRuntime

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("1. Planning execution...")
    engine = PipelineEngine()
    request = PipelineRequest(title="Sprint 10 PR1", touches_database=False)
    run = engine.plan(request)
    
    print("\n2. Initializing Runtime...")
    provider = NineRouterProvider()
    runtime = ExecutionRuntime(provider=provider)
    
    print(f"\n3. Executing Pipeline: {run.name}")
    try:
        runtime.execute(run, instructions="Say hello briefly!")
        
        print("\n4. Pipeline Results:")
        for result in run.results:
            print(f"[{result.agent.role}]")
            print(f"[PASS] Completed in {result.duration_seconds}s")
            print(f"Output: {result.output.strip()}\n")
            
        print("Pipeline completed successfully.")
    except Exception as e:
        print(f"\n[FAIL] Pipeline halted due to failure: {str(e)}")

if __name__ == "__main__":
    main()