from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    supabase_url: str
    supabase_key: str

    jwt_key: str
    jwt_algorithm: str = "HS256"
    jwt_time: int = 60

settings = Settings()