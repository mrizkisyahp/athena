from app.planning.service import ExecutionPlanner
from app.responsibilities.models import ResponsibilityPriority, Responsibility
from app.services.time_service import TimeService
from app.time.duration import Duration
from app.workload.models import WorkloadAnalysis


class WorkloadBalancer:
    def __init__(self, planner: ExecutionPlanner):
        self._planner = planner

    def _is_protected(self, task: Responsibility, now) -> bool:
        if task.priority == ResponsibilityPriority.CRITICAL:
            return True
        if task.due_date:
            if task.due_date.date() <= now.date():
                return True
        return False

    def analyze(self, available_capacity: Duration) -> WorkloadAnalysis:
        plan = self._planner.generate_plan()
        
        if plan.total_estimated_duration is None:
            return WorkloadAnalysis(
                total_workload=None,
                available_capacity=available_capacity,
                overloaded=False,
                suggested_deferrals=[],
                reasoning=["Today's total workload is unknown because some responsibilities are missing time estimates. Athena cannot confidently recommend deferrals."]
            )

        if plan.total_estimated_duration.minutes <= available_capacity.minutes:
            return WorkloadAnalysis(
                total_workload=plan.total_estimated_duration,
                available_capacity=available_capacity,
                overloaded=False,
                suggested_deferrals=[],
                reasoning=["Your available capacity is sufficient for today's planned workload."]
            )
            
        now = TimeService.now()
        required_minutes = plan.total_estimated_duration.minutes - available_capacity.minutes
        
        unprotected_tasks = [t for t in plan.responsibilities if not self._is_protected(t, now) and t.estimated_duration]
        
        best_deferrals = None
        best_score = None
        
        if len(unprotected_tasks) <= 15:
            import itertools
            for r in range(1, len(unprotected_tasks) + 1):
                for subset in itertools.combinations(unprotected_tasks, r):
                    removed = sum(t.estimated_duration.minutes for t in subset)
                    if removed >= required_minutes:
                        remaining = [t for t in plan.responsibilities if t not in subset]
                        switches = 0
                        prev = None
                        for t in remaining:
                            if t.project_id != prev:
                                if prev is not None:
                                    switches += 1
                                prev = t.project_id
                        
                        idx_sum = sum(plan.responsibilities.index(t) for t in subset)
                        score = (switches, len(subset), removed, -idx_sum)
                        
                        if best_score is None or score < best_score:
                            best_score = score
                            best_deferrals = list(subset)

        used_optimization = False
        if best_deferrals is not None:
            deferrals = best_deferrals
            used_optimization = True
            current_workload = plan.total_estimated_duration.minutes - sum(t.estimated_duration.minutes for t in deferrals)
        else:
            current_workload = plan.total_estimated_duration.minutes
            deferrals = []
            for task in reversed(plan.responsibilities):
                if current_workload <= available_capacity.minutes:
                    break
                    
                if self._is_protected(task, now):
                    continue
                    
                if task.estimated_duration:
                    deferrals.append(task)
                    current_workload -= task.estimated_duration.minutes

        if not deferrals:
            return WorkloadAnalysis(
                total_workload=plan.total_estimated_duration,
                available_capacity=available_capacity,
                overloaded=True,
                suggested_deferrals=[],
                reasoning=["Your workload exceeds today's capacity, but no safe responsibilities can be deferred."]
            )
            
        if current_workload > available_capacity.minutes:
            reasoning = [
                "Today's workload exceeds your available capacity.",
                "The suggested responsibilities are the lowest-risk items to move.",
                "Even with these deferrals, you may still be overloaded because the remaining tasks are protected."
            ]
        else:
            reasoning = [
                "Today's workload exceeds your available capacity.",
                "The suggested responsibilities are the lowest-risk items to move.",
                "Critical responsibilities due today remain protected."
            ]
            
        if used_optimization:
            reasoning.append("Related work was kept together where possible to preserve focus and reduce unnecessary context switching.")
            
        return WorkloadAnalysis(
            total_workload=plan.total_estimated_duration,
            available_capacity=available_capacity,
            overloaded=True,
            suggested_deferrals=deferrals,
            reasoning=reasoning
        )
