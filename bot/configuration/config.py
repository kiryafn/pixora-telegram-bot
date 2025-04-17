from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    database_url: str = Field(..., env="DATABASE_URL")

    # базовый URL и ключ для job‑API
    job_api_url: str = Field(..., env="JOB_API_URL")
    job_api_key: str | None = Field(None, env="JOB_API_KEY")

    # какие-то дополнительные настройки
    # polling_timeout: int = Field(30, env="POLLING_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()