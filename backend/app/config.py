from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    model_name: str = "qwen3:1.7b"
    ollama_host: str = "http://localhost:11434"
    cors_origins: str = "http://localhost:3000"
    upload_dir: str = "backend/app/uploads"
    max_upload_mb: int = 50

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
