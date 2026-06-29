from pathlib import Path
from app.logging.logger import logger


class PromptService:
    def __init__(self) -> None:
        self._prompt_dir = Path(__file__).parent.parent / "prompts"

        self._cache: dict[str, str] = {}

    def load(self, name: str) -> str:

        if name in self._cache:
            logger.info(
                "Loading prompt from cache",
                prompt_name=name,
            )

            return self._cache[name]

        logger.info(
            "Loading prompt from disk",
            prompt_name=name,
            prompt_path=self._prompt_dir / f"{name}.md",
        )

        prompt = (
            self._prompt_dir / f"{name}.md"
        ).read_text(encoding="utf-8")

        self._cache[name] = prompt

        return prompt