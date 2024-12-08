from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.models.database import init_db
from app.routes.home import router as home_router
from app.routes.lti import router as lti_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG_MODE, lifespan=lifespan)

app.include_router(lti_router)
app.include_router(home_router)
