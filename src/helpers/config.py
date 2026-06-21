from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    FILE_TYPE: list[str]
    FILE_SIZE_LIMIT: int
    FILE_CHUNK_SIZE: int

    MONGODB_URl: str
    MONGODB_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_settings():
    return Settings()