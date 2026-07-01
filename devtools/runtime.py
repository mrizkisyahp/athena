from devtools.models import PipelineRun, AgentResult
from devtools.config import ProfileRegistry
from devtools.prompt_library import PromptLibrary
from devtools.providers.base import BaseProvider
from devtools.providers.models import ProviderRequest

class ExecutionRuntime:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.prompt_library = PromptLibrary()

    def execute(self, run: PipelineRun, instructions: str) -> None:
        """
        Executes the planned agents in sequential order. 
        Halts immediately on the first exception.
        """
        for agent in run.planned_agents:
            # 1. Resolve the profile
            profile = ProfileRegistry.resolve(agent)

            # 2. Resolve the prompt
            prompt_content = self.prompt_library.get_prompt(agent)

            # 3. Build the provider request
            request = ProviderRequest(
                agent=agent,
                profile=profile,
                instructions=instructions,
                prompt=prompt_content
            )

            # 4. Execute via provider
            # We intentionally let exceptions bubble up (no retries/recovery).
            response = self.provider.execute(request)

            # 5. Record the result
            result = AgentResult(
                agent=agent,
                output=response.output,
                duration_seconds=response.duration_seconds
            )
            run.results.append(result)
