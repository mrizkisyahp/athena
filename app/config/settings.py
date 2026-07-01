from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Athena"
    app_env: str = "development"

    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""
    
    # DevTools Configuration
    devtools_ninerouter_api_key: str = ""
    devtools_ninerouter_base_url: str = "http://localhost:20128/v1"
    
    devtools_architect_model: str = ""
    devtools_backend_executor_model: str = ""
    devtools_database_reviewer_model: str = ""
    devtools_qa_reviewer_model: str = ""

    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()