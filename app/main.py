from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.users_controller import router as users_router
from app.db.mongo import close_mongo_connection, connect_to_mongo
from app.routers.health import router as health_router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        connect_to_mongo()
        try:
            yield
        finally:
            close_mongo_connection()

    app = FastAPI(
        title="yms-appt-service",
        description="YMS Appointment Service API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {"name": "health", "description": "Service health endpoints"},
            {"name": "users", "description": "User CRUD endpoints"},
        ],
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # adjust to specific domains in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(users_router)
    return app


app = create_app()

