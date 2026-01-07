from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.all_models import Job

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_jobs(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    
    jobs = query.limit(50).all()
    
    # Return simple dict representation (Pydantic models should be used in prod)
    results = []
    for j in jobs:
        results.append({
            "job_id": str(j.job_id),
            "erp_job": j.erp_job_number,
            "part": j.part_number,
            "status": j.status,
            "customer": j.customer_name,
            "qty": j.quantity_required
        })
    return results

@router.get("/{job_id}")
def get_job_detail(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": str(job.job_id),
        "erp_job": job.erp_job_number,
        "part": job.part_number,
        "status": job.status,
        "details": {
            "customer": job.customer_name,
            "material": job.material,
            "thickness": float(job.thickness) if job.thickness else 0.0,
            "due": job.due_date
        },
        "runtime": {
            "actual": float(job.actual_runtime_seconds or 0)
        }
    }
