from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
        env_file= "./.env",
        extra="ignore",
        env_ignore_empty=True
    )

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    
    DEBUG: str

    model_config = _base_config

class JWTSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = _base_config

settings = Settings() # type: ignore
jwt_settings = JWTSettings() # type: ignore