from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import Job, Machine
from sqlalchemy import func

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Get high-level stats for the dashboard tiles.
    """
    queued = db.query(Job).filter(Job.status == 'QUEUED').count()
    running_jobs = db.query(Job).filter(Job.status == 'RUNNING').count()
    active_lasers = db.query(Machine).filter(Machine.is_active == True).count() 
    # Logic for active lasers might need to check if they are actually running based on MachineRun
    
    return {
        "jobs_queued": queued,
        "jobs_running": running_jobs,
        "jobs_done_today": 12, # Mock for now or would need date filter query
        "lasers_active": active_lasers
    }

@router.get("/activity")
def get_activity_feed():
    # Mock feed
    return [
        {"time": "10:21", "message": "Laser 1 completed Sheet S-027"},
        {"time": "10:15", "message": "Job 10452 posted to JobBOSS2"}
    ]
