from sqlalchemy import Column, Integer, String, Float, DateTime , Boolean
from app.models import Base
from sqlalchemy.sql import func


# برای Alembic مستقیم Base بساز
class Lawyer(Base):
    __tablename__ = "lawyers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    phone = Column(String(15), nullable=False) 
    license_number = Column(String(100), unique=True, index=True, nullable=False)
    specialization = Column(String(255))
    experience_years = Column(Integer, default=0) 
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
