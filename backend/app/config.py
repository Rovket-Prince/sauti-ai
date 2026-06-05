from pydantic_settings import BaseSettings, SettingsConfigForm

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    # This tells pydantic to look for a .env file one level up from the app directory
    model_config = SettingsConfigForm(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()