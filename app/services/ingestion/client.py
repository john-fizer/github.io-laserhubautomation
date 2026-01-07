import random
from datetime import datetime, timedelta
from typing import List, Dict

class JobBOSSClient:
    """
    Mock client for JobBOSS2 API.
    In production, this would use requests to hit the actual ERP endpoints.
    """
    
    def __init__(self, api_url: str = None, api_key: str = None):
        self.api_url = api_url
        self.api_key = api_key

    def get_new_jobs(self) -> List[Dict]:
        """
        Simulate fetching jobs that are 'Released' and ready for production.
        """
        # Return some realistic mock data
        mock_jobs = [
            {
                "Job": "10452",
                "Customer": "ACME Parts",
                "Part_Number": "PART-AX123",
                "Material": "A36",
                "Thickness": 0.500,
                "Qty_Order": 250,
                "Due_Date": (datetime.now() + timedelta(days=2)).isoformat(),
                "Priority": "Normal"
            },
            {
                "Job": "10453",
                "Customer": "Cyberdyne",
                "Part_Number": "SKY-NET-01",
                "Material": "SS304",
                "Thickness": 0.125,
                "Qty_Order": 80,
                "Due_Date": (datetime.now() + timedelta(days=1)).isoformat(),
                "Priority": "High"
            },
            {
                "Job": "10460",
                "Customer": "Wayne Ent",
                "Part_Number": "BAT-WING-07",
                "Material": "AL5052",
                "Thickness": 0.063,
                "Qty_Order": 40,
                "Due_Date": (datetime.now() + timedelta(days=5)).isoformat(),
                "Priority": "Low"
            }
        ]
        return mock_jobs

    def update_job_status(self, job_number: str, status: str, hours: float, qty: int):
        """
        Simulate pushing data back to JobBOSS.
        """
        print(f"[JB2-MOCK] Updating Job {job_number}: Status={status}, Hours={hours}, Qty={qty}")
        return True
