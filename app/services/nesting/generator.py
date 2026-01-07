import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.all_models import Job
from app.core.config import get_settings

settings = get_settings()

class NestExportService:
    def __init__(self, db: Session):
        self.db = db
        self.export_path = settings.HOT_FOLDER_PATH

    def export_queued_jobs(self):
        """
        Find QUEUED jobs and write them to a CSV for Smart System.
        """
        # Get jobs
        jobs = self.db.query(Job).filter(Job.status == 'QUEUED').all()
        
        if not jobs:
            return 0

        # Ensure directory exists
        os.makedirs(self.export_path, exist_ok=True)
        
        filename = f"Import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.export_path, filename)
        
        # Write CSV
        with open(filepath, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Header expected by Smart System (Hypothetical)
            writer.writerow(['JobNumber', 'PartName', 'Material', 'Thickness', 'Qty', 'DueDate'])
            
            for job in jobs:
                writer.writerow([
                    job.erp_job_number,
                    job.part_number,
                    job.material,
                    job.thickness,
                    job.quantity_required - job.quantity_completed,
                    job.due_date.strftime('%Y-%m-%d')
                ])
                
                # Update status to NESTING
                job.status = 'NESTING'
        
        self.db.commit()
        return len(jobs)
