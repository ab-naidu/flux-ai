from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    # v2 verify (see https://www.unkey.com/docs ) — api.unkey.dev often fails DNS; use .com
    unkey_verify_url: str = "https://api.unkey.com/v2/keys.verifyKey"
    # Required when UNKEY_ENABLED=true: Unkey dashboard → Root key (Bearer for verify API)
    unkey_root_key: str = ""
    unkey_enabled: bool = True
    railtracks_enabled: bool = False
    # Optional: POST JSON trace events for Railtracks / external audit sinks
    railtracks_webhook_url: str = ""
    # If empty, /api/inventory/sync uses an in-process mock (safe for demos).
    mock_inventory_url: str = ""


settings = Settings()
