from fastapi import APIRouter
from app.api.endpoints import dashboard, jobs, machines

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(machines.router, prefix="/machines", tags=["machines"])
