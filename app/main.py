from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import lti
from .models.database import init_db
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG_MODE,
    lifespan=lifespan
)

app.include_router(lti.router)