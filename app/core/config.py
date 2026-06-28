from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Vision Agent Backend MVP"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./data/vision_agent.db"
    upload_dir: Path = Path("./data/uploads")
    result_dir: Path = Path("./data/results")
    yolo_model_name: str = "yolov8n.pt"
    confidence_threshold: float = 0.35

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.result_dir.mkdir(parents=True, exist_ok=True)
    return settings
