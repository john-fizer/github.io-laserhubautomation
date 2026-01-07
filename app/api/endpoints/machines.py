from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import Machine

router = APIRouter()

@router.get("/")
def get_machines(db: Session = Depends(get_db)):
    machines = db.query(Machine).all()
    return [{"id": m.machine_id, "name": m.name, "url": m.mtconnect_url} for m in machines]

@router.post("/trigger_run/{program_name}")
def trigger_manual_run_completion(program_name: str, duration: int, db: Session = Depends(get_db)):
    """
    Dev endpoint to manually trigger a run completion for testing the calculator.
    """
    from app.models.all_models import MachineRun
    from app.services.allocation.calculator import TimeAllocationEngine
    from datetime import datetime
    import uuid

    # Create dummy run
    run = MachineRun(
        run_id=uuid.uuid4(),
        machine_id=1, # Assume 1 exists
        nc_program_name=program_name,
        start_time=datetime.now(),
        end_time=datetime.now(),
        actual_runtime_seconds=duration
    )
    db.add(run)
    db.commit()
    
    # Allocator
    allocator = TimeAllocationEngine(db)
    allocator.allocate_run(run.run_id)
    
    return {"status": "Complete", "allocated_seconds": duration}
