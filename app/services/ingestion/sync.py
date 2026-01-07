from sqlalchemy.orm import Session
from app.models.all_models import Job
from app.services.ingestion.client import JobBOSSClient
from datetime import datetime

class IngestionWorker:
    def __init__(self, db: Session):
        self.db = db
        self.client = JobBOSSClient()

    def sync_jobs(self):
        """
        Fetch new jobs and upsert into local DB.
        """
        raw_jobs = self.client.get_new_jobs()
        synced_count = 0
        
        for rj in raw_jobs:
            # Check if exists
            existing = self.db.query(Job).filter(Job.erp_job_number == rj['Job']).first()
            
            if not existing:
                new_job = Job(
                    erp_job_number=rj['Job'],
                    customer_name=rj['Customer'],
                    part_number=rj['Part_Number'],
                    material=rj['Material'],
                    thickness=rj['Thickness'],
                    quantity_required=rj['Qty_Order'],
                    due_date=datetime.fromisoformat(rj['Due_Date']),
                    status='QUEUED'
                )
                self.db.add(new_job)
                synced_count += 1
            else:
                # Update logic if needed (e.g. qty changes)
                pass
        
        self.db.commit()
        return synced_count
