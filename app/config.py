from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_service_account_file: str

    class Config:
        env_file = ".env"

settings = Settings()  # type: ignore
