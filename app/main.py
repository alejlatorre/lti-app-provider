from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.models.database import init_db
from app.routes import home_app, lti


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


home = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG_MODE, lifespan=lifespan)

home.include_router(lti.router)
home.include_router(home_app.router)
