from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    SRC_PORT: int
    DOCKER_PORT: int

    SECRET_KEY: str = 'secret_key :)'
    ALGORITHM: str = 'HS256'

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str


settings = Settings()
