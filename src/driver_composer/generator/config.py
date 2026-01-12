from pydantic_settings import BaseSettings


class Config(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-5.1"

    class Config:
        env_file = ".env"


conf = Config()
