from dataclasses import dataclass

@dataclass(slots=True)
class Agent:
    name: str
    role: str
    provider: str
    model: str

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
class PipelineRun:
    name: str
    results: list['AgentResult']

@dataclass(slots=True)
class PipelineReport:
    stage: str
    completed: bool
    summary: str
