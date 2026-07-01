from app.awareness.models import Insight

class InsightPromptBuilder:
    @staticmethod
    def build(insights: list[Insight]) -> str:
        if not insights:
            return ""
            
        lines = ["Current Insights\n"]
        for insight in insights:
            lines.append(f"- [{insight.severity.value.upper()}] {insight.title}")
            lines.append(f"  {insight.description}\n")
            
        return "\n".join(lines)
