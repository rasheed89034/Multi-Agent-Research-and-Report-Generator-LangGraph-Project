from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # exposes provider keys (ANTHROPIC_API_KEY etc.) to LangChain


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    llm_main: str = "anthropic:claude-sonnet-5-5"   # planner, critic, writer
    llm_fast: str = "anthropic:claude-haiku-5-5"    # researcher extraction
    db_path: str = "checkpoints.sqlite"
    max_iterations: int = 2                          # max critic -> researcher retry rounds
    cors_origins: list[str] = ["http://localhost:3000"]
    max_tokens: int | None = None


settings = Settings()
