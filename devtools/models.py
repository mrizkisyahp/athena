from dataclasses import dataclass, field

@dataclass(slots=True)
class Agent:
    name: str
    role: str
    provider: str
    model: str
    is_conditional: bool = False

@dataclass(slots=True)
class Task:
    title: str
    instructions: str

@dataclass(slots=True)
class AgentResult:
    agent: Agent
    output: str
    duration_seconds: float | None = None

@dataclass(slots=True)
class PipelineRequest:
    title: str
    touches_database: bool = False

@dataclass(slots=True)
class PipelineRun:
    name: str
    planned_agents: list[Agent] = field(default_factory=list)
    results: list[AgentResult] = field(default_factory=list)

@dataclass(slots=True)
class PipelineReport:
    stage: str
    completed: bool
    summary: str
