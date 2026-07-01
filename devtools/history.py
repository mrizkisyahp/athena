from devtools.models import PipelineRun

class RunHistory:
    def __init__(self):
        self._runs: list[PipelineRun] = []
        
    def add(self, run: PipelineRun):
        self._runs.append(run)
        
    def get_all(self) -> list[PipelineRun]:
        return self._runs
        
    def get(self, name: str) -> PipelineRun | None:
        for run in self._runs:
            if run.name == name:
                return run
        return None
