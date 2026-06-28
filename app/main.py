from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.session import Base, engine


def create_app() -> FastAPI:
    settings = get_settings()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.app_name,
        description="Image upload, YOLO inference, and result metadata management API.",
        version="0.1.0",
    )
    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
