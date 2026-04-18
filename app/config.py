from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    
    DEBUG: str

    model_config = SettingsConfigDict(
        env_file= "./.env",
        extra="ignore",
        env_ignore_empty=True
    )

settings = Settings() # type: ignore