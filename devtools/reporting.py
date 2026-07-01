from devtools.models import PipelineRun, PipelineReport

class ReportBuilder:
    @classmethod
    def success(cls, run: PipelineRun) -> PipelineReport:
        return PipelineReport(
            stage="Runtime",
            completed=True,
            summary="Pipeline completed successfully."
        )
        
    @classmethod
    def failure(cls, run: PipelineRun, exception: Exception) -> PipelineReport:
        failed_stage = "Unknown"
        if len(run.results) < len(run.planned_agents):
            failed_stage = run.planned_agents[len(run.results)].name
            
        return PipelineReport(
            stage="Runtime",
            completed=False,
            summary=f"Pipeline halted while executing {failed_stage}. Error: {str(exception)}"
        )
