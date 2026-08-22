import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.logging import logger
from app.db.mongodb import init_db, close_db, get_database
from app.db.seed import seed_database
from app.routes import auth, users, assessments, problems, sessions, tutor, learner

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing CodeMentor AI Backend...")
    await init_db()
    db = get_database()
    await seed_database(db)
    logger.info("Database and Seed Data Ready. CodeMentor AI is running.")
    yield
    logger.info("Shutting down CodeMentor AI Backend...")
    await close_db()

app = FastAPI(
    title="CodeMentor AI - Adaptive AI Coding Tutor API",
    description="Backend services for CodeMentor AI, featuring progressive hints, server-side answer locking, knowledge checks, and adaptive learner profile modeling.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assessments.router)
app.include_router(problems.router)
app.include_router(sessions.router)
app.include_router(tutor.router)
app.include_router(learner.router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "service": "CodeMentor AI Backend",
        "version": "1.0.0",
        "model": settings.GEMINI_MODEL,
        "gemini_configured": settings.is_gemini_configured
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "db": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main.py:app", host="0.0.0.0", port=8000, reload=True)
