"""Configuration management for Datto RMM MCP server."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Datto RMM API settings."""

    api_key: str = ""
    api_secret: str = ""
    api_url: str = "https://merlot-api.centrastage.net/api"
    auth_url: str = "https://merlot-api.centrastage.net/auth/oauth/token"
    timeout: float = 30.0
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_prefix="DATTORMM_",
        env_file=".env"
    )

    def is_configured(self) -> bool:
        """Check if required credentials are set."""
        return bool(self.api_key and self.api_secret)


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get or create settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset settings for testing."""
    global _settings
    _settings = None
