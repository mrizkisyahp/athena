class BriefingFormatter:
    @staticmethod
    def build(
        schedule_context: str,
        memory_context: str,
        insight_context: str,
    ) -> str:
        sections = []

        if schedule_context:
            sections.append(schedule_context.strip())

        if memory_context:
            sections.append(memory_context.strip())

        if insight_context:
            sections.append(insight_context.strip())

        return "\n\n".join(sections)
