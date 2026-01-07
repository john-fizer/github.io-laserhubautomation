import pandas as pd
import os
from sqlalchemy.orm import Session
from app.models.all_models import Sheet, SheetPart, Job
from app.core.config import get_settings

class NestImportService:
    def __init__(self, db: Session):
        self.db = db

    def process_report(self, filepath: str):
        """
        Parse a completed nest report and create Sheet/SheetPart records.
        """
        # Assume CSV format: SheetName, Program, Material, Thickness, PlannedTime, Job, Part, Qty, CutLength
        try:
            df = pd.read_csv(filepath)
            
            # Group by unique Sheet
            unique_sheets = df['SheetName'].unique()
            
            for sheet_name in unique_sheets:
                sheet_rows = df[df['SheetName'] == sheet_name]
                first_row = sheet_rows.iloc[0]
                
                # Create Sheet
                new_sheet = Sheet(
                    nc_program_name=str(first_row['Program']),
                    material=str(first_row['Material']),
                    thickness=float(first_row['Thickness']),
                    planned_runtime_seconds=float(first_row['PlannedTime']),
                    status='PLANNED'
                )
                self.db.add(new_sheet)
                self.db.flush() # Get ID
                
                # Create Parts
                for _, row in sheet_rows.iterrows():
                    # Find Job
                    job_num = str(row['Job'])
                    job = self.db.query(Job).filter(Job.erp_job_number == job_num).first()
                    
                    if job:
                        part = SheetPart(
                            sheet_id=new_sheet.sheet_id,
                            job_id=job.job_id,
                            quantity_on_sheet=int(row['Qty']),
                            cut_length_total=float(row['CutLength'])
                        )
                        self.db.add(part)
                        
                        # Update Job Status
                        if job.status == 'NESTING':
                            job.status = 'SCHEDULED'
            
            self.db.commit()
            return len(unique_sheets)
            
        except Exception as e:
            print(f"Error processing report {filepath}: {e}")
            self.db.rollback()
            return 0
