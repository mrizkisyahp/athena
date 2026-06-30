from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Athena"
    app_env: str = "development"

    openrouter_api_key: str = ""

    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""

    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()