from pydantic import Field
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    database_url: str = Field(validation_alias="DATABASE_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()