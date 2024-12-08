from fastapi import FastAPI
from .routes import lti
from .models.database import init_db
from .config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG_MODE
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(lti.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 