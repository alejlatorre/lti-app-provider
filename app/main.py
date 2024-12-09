from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.models.database import init_db
from app.routes.home import router as home_router
from app.routes.lti import router as lti_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[settings.LTI_AUTH_TOKEN_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
]

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG_MODE,
    lifespan=lifespan,
    middleware=middleware,
)

app.include_router(lti_router)
app.include_router(home_router)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = f"ALLOW-FROM {settings.LTI_ISSUER}"
    response.headers["Content-Security-Policy"] = (
        f"frame-ancestors 'self' {settings.LTI_ISSUER}"
    )
    return response
