from fastapi import FastAPI
from app.core.config import get_settings
from app.models import all_models
from app.core.database import engine

# Create tables
all_models.Base.metadata.create_all(bind=engine)

settings = get_settings()

from app.api.api import api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to LaserFlow Automation API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app",
                host="0.0.0.0", port = int(os.getenv("PORT",8000)), reload = True)

