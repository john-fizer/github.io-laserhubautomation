from sqlalchemy.orm import Session
from app.models.all_models import MachineRun, Sheet, SheetPart, Job

class TimeAllocationEngine:
    def __init__(self, db: Session):
        self.db = db

    def allocate_run(self, run_id: str):
        """
        Distribute the actual runtime of a MachineRun to its constituent Jobs.
        """
        run = self.db.query(MachineRun).filter(MachineRun.run_id == run_id).first()
        if not run:
            print(f"Run {run_id} not found.")
            return

        if not run.nc_program_name:
            print(f"Run {run_id} has no program name.")
            return

        # 1. Find Sheet
        sheet = self.db.query(Sheet).filter(Sheet.nc_program_name == run.nc_program_name).first()
        if not sheet:
            print(f"Orphan run: Program {run.nc_program_name} has no matching Sheet.")
            return

        # Link run to sheet
        run.sheet_id = sheet.sheet_id
        
        # 2. Get Parts and Total Basis
        parts = sheet.parts
        total_cut_length = sum(p.cut_length_total for p in parts)
        
        if total_cut_length == 0:
            print("Total cut length is 0, cannot allocate.")
            return

        # 3. Distribute Time
        actual_seconds = run.actual_runtime_seconds or 0
        
        print(f"Allocating {actual_seconds}s across {len(parts)} parts. Total Len: {total_cut_length}")

        for part in parts:
            weight = float(part.cut_length_total) / float(total_cut_length)
            allocated = int(actual_seconds * weight)
            
            # Update Part
            part.allocated_runtime_seconds = (part.allocated_runtime_seconds or 0) + allocated
            
            # Update Job
            job = part.job
            job.actual_runtime_seconds = (job.actual_runtime_seconds or 0) + allocated
            
            # Check Completion (Simple logic: if sheet is done, assuming job part on this sheet is done)
            # In reality, check if job.quantity_completed + part.quantity_on_sheet >= job.quantity_required
            # For now, we just accumulate time.
            
            print(f"  -> Job {job.erp_job_number}: +{allocated}s")

        sheet.status = 'COMPLETE'
        self.db.commit()
