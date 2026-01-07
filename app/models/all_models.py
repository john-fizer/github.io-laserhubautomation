import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Job(Base):
    __tablename__ = "jobs"
    
    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    erp_job_number = Column(String(50), unique=True, nullable=False)
    customer_name = Column(String(100))
    part_number = Column(String(100))
    material = Column(String(50))
    thickness = Column(DECIMAL(10, 4))
    quantity_required = Column(Integer)
    quantity_completed = Column(Integer, default=0)
    due_date = Column(DateTime)
    status = Column(String(20), default='QUEUED') # QUEUED, NESTING, RUNNING, DONE
    actual_runtime_seconds = Column(DECIMAL(12, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    sheet_parts = relationship("SheetPart", back_populates="job")

class Sheet(Base):
    __tablename__ = "sheets"
    
    sheet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nc_program_name = Column(String(100), nullable=False) # The link between Digital and Physical
    machine_id = Column(Integer, ForeignKey("machines.machine_id"))
    material = Column(String(50))
    thickness = Column(DECIMAL(10, 4))
    planned_runtime_seconds = Column(DECIMAL(12, 2))
    status = Column(String(20), default='PLANNED')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    parts = relationship("SheetPart", back_populates="sheet")
    machine_runs = relationship("MachineRun", back_populates="sheet")
    machine = relationship("Machine", back_populates="sheets")

class SheetPart(Base):
    __tablename__ = "sheet_parts"
    
    sheet_part_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sheet_id = Column(UUID(as_uuid=True), ForeignKey("sheets.sheet_id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"))
    quantity_on_sheet = Column(Integer)
    cut_length_total = Column(DECIMAL(12, 2)) # Used for weighting time
    allocated_runtime_seconds = Column(DECIMAL(12, 2), default=0.0)
    
    sheet = relationship("Sheet", back_populates="parts")
    job = relationship("Job", back_populates="sheet_parts")

class Machine(Base):
    __tablename__ = "machines"
    
    machine_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    mtconnect_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    sheets = relationship("Sheet", back_populates="machine")
    runs = relationship("MachineRun", back_populates="machine")

class MachineRun(Base):
    __tablename__ = "machine_runs"
    
    run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    machine_id = Column(Integer, ForeignKey("machines.machine_id"))
    nc_program_name = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_runtime_seconds = Column(Integer)
    sheet_id = Column(UUID(as_uuid=True), ForeignKey("sheets.sheet_id"), nullable=True)
    
    machine = relationship("Machine", back_populates="runs")
    sheet = relationship("Sheet", back_populates="machine_runs")
