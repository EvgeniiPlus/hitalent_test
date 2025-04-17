from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    LOG_LEVEL: str = 'INFO'

    class Config:
        env_file = ".env"


settings = Settings()
