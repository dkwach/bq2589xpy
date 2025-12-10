from pydantic_settings import BaseSettings


class Config(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-5-nano"

    class Config:
        env_file = ".env"


conf = Config()
