from app.core.database import SessionLocal, engine
from app.models import all_models
from app.services.ingestion.sync import IngestionWorker
from app.services.nesting.generator import NestExportService
from app.services.nesting.file_watcher import NestImportService
from app.services.allocation.calculator import TimeAllocationEngine
from app.models.all_models import MachineRun, Machine
from datetime import datetime
import os
import uuid

def verify_flow():
    # 1. Setup DB
    print("1. Creating Database Tables...")
    all_models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create a machine
    if not db.query(Machine).first():
        db.add(Machine(name="Laser 1", mtconnect_url="http://mock", is_active=True))
        db.commit()

    # 2. Ingestion
    print("\n2. Running Ingestion (Mock JB2)...")
    ingest = IngestionWorker(db)
    count = ingest.sync_jobs()
    print(f"   -> Imported {count} jobs.")

    # 3. Nest Export
    print("\n3. Running Nest Export...")
    exporter = NestExportService(db)
    exported = exporter.export_queued_jobs()
    print(f"   -> Exported {exported} jobs to Hot Folder.")

    # 4. Simulate Nest Output (Import)
    print("\n4. Simulating Nest Result (L1-TEST.MIN using Job 10452)...")
    # Manually creating sheet/sheetpart because we don't have a CSV to parse in this script easily
    # But essentially NestImportService does this.
    
    from app.models.all_models import Sheet, SheetPart, Job
    job = db.query(Job).filter(Job.erp_job_number == "10452").first()
    if job:
        sheet = Sheet(
            nc_program_name="L1-TEST.MIN",
            machine_id=1,
            material="A36",
            thickness=0.5,
            planned_runtime_seconds=600,
            status='PLANNED'
        )
        db.add(sheet)
        db.flush()
        
        part = SheetPart(
            sheet_id=sheet.sheet_id,
            job_id=job.job_id,
            quantity_on_sheet=50,
            cut_length_total=100.0 # Only one part, so 100% weight
        )
        db.add(part)
        db.commit()
        print("   -> Created Sheet 'L1-TEST.MIN' with Job 10452.")

    # 5. Machine Run Completion
    print("\n5. Simulating Machine Run Completion...")
    run = MachineRun(
        run_id=uuid.uuid4(),
        machine_id=1,
        nc_program_name="L1-TEST.MIN",
        start_time=datetime.now(),
        end_time=datetime.now(),
        actual_runtime_seconds=650 # 50s slower than planned
    )
    db.add(run)
    db.commit()
    print(f"   -> Created Run {run.run_id} for 'L1-TEST.MIN' (650s).")

    # 6. Allocation
    print("\n6. Running Time Allocation Engine...")
    allocator = TimeAllocationEngine(db)
    allocator.allocate_run(run.run_id)

    # 7. Check Result
    db.refresh(job)
    print(f"\n[RESULT] Job 10452 Actual Runtime: {job.actual_runtime_seconds}s")
    
    if int(job.actual_runtime_seconds) == 650:
        print("SUCCESS: Full runtime allocated to the single job on sheet.")
    else:
        print("FAILURE: Runtime mismatch.")

if __name__ == "__main__":
    verify_flow()
