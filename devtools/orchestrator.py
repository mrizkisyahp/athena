from devtools.models import PipelineRequest, PipelineRun
from devtools.engine import PipelineEngine
from devtools.runtime import ExecutionRuntime
from devtools.history import RunHistory
from devtools.reporting import ReportBuilder

class PipelineOrchestrator:
    def __init__(self, engine: PipelineEngine, runtime: ExecutionRuntime, history: RunHistory):
        self.engine = engine
        self.runtime = runtime
        self.history = history

    def execute_pipeline(self, request: PipelineRequest, instructions: str) -> PipelineRun:
        # 1. Plan
        run = self.engine.plan(request)
        
        # 2. Execute
        try:
            self.runtime.execute(run, instructions)
            # 3a. Report Success
            run.report = ReportBuilder.success(run)
        except Exception as e:
            # 3b. Report Failure
            run.report = ReportBuilder.failure(run, e)
            
        # 4. Record History
        self.history.add(run)
        
        # 5. Return
        return run
