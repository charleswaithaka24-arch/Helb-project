"""
Application configuration using pydantic-settings.
Loads sensitive data from .env file and provides type-safe configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    """Application configuration with environment variable loading."""

    # Application metadata
    project_name: str = Field("backend", validation_alias="PROJECT_NAME")
    project_version: str = Field("0.1.0", validation_alias="PROJECT_VERSION")

    # Database configuration
    database_url: str = Field("sqlite:///./backend.db", validation_alias="DATABASE_URL")

    # Security configuration
    secret_key: str = Field("changeme", validation_alias="SECRET_KEY")

    # Africa's Talking SMS configuration
    africastalking_username: str = Field("your_username", validation_alias="AFRICASTALKING_USERNAME")
    africastalking_api_key: str = Field("your_api_key", validation_alias="AFRICASTALKING_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global configuration instance
config = Config()  # type: ignore