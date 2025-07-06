from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.database import init_db
from app.api.startup import router as startup_router
from app.api.chat import router as chat_router

setup_logging()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

# Mount API routers
app.include_router(startup_router)
app.include_router(chat_router)