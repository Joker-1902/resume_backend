from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import ClassVar

class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")
    URL: str


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra='ignore')
    SECRET: SecretStr
    ALGORITHM: str = "HS256"


class Settings(BaseSettings):
    database: ClassVar[DataBaseSettings] = DataBaseSettings()
    jwt_settings: ClassVar[JWTSettings] = JWTSettings()


settings = Settings()

