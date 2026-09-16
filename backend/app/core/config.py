"""
Application configuration.

All values are read from environment variables so the same code can run
unchanged in local dev, Docker Compose, and AWS/Kubernetes -- only the
environment variables change between environments.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Full SQLAlchemy connection string, e.g.
    # postgresql+psycopg2://user:password@host:5432/dbname
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/employee_task_db"

    # "local" | "docker" | "production"
    environment: str = "local"

    # Comma-separated list of origins allowed to call the API (CORS).
    # In production this should be your real frontend domain(s).
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
