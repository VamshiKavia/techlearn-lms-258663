from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.logging import configure_logging, get_logger
from src.core.errors import register_exception_handlers
from src.api.v1.routes.health import router as health_router
from src.api.v1.routes.courses import router as courses_router
from src.db.mongo import connect_to_mongo, close_mongo_connection

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application with routes, middleware, error handlers, and startup/shutdown events.
    """
    settings = get_settings()

    app = FastAPI(
        title="TechLearn LMS API",
        version="0.1.0",
        description="Learning Management System backend API for courses, users, enrollments, and more.",
        contact={"name": "TechLearn", "url": "https://example.com"},
        license_info={"name": "Proprietary"},
        openapi_tags=[
            {"name": "Health", "description": "Service health and diagnostics"},
            {"name": "Courses", "description": "Course catalog operations"},
        ],
    )

    # Configure logging
    configure_logging(settings)
    logger = get_logger(__name__)
    logger.info("Starting TechLearn LMS API", extra={"env": settings.APP_ENV})

    # CORS
    allow_origins: List[str] = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health_router)
    app.include_router(courses_router, prefix="/api/v1", tags=["Courses"])

    # Errors
    register_exception_handlers(app)

    # Startup / Shutdown
    @app.on_event("startup")
    async def on_startup():
        await connect_to_mongo()

    @app.on_event("shutdown")
    async def on_shutdown():
        await close_mongo_connection()

    return app


app = create_app()


if __name__ == "__main__":
    # Allow running directly: python -m src.api.main
    settings = get_settings()
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.APP_ENV == "development",
    )
