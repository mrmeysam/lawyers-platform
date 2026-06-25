from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LawyerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., max_length=15)
    license_number: str = Field(..., max_length=100)
    specialization: Optional[str] = None
    experience_years: Optional[int] = 0
    # تغییر: از city (رشته) به city_id (عدد) تغییر دادیم
    city_id: Optional[int] = None

class LawyerCreate(LawyerBase):
    pass

class LawyerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    # تغییر: اینجا هم city_id اضافه شد تا بتوانیم شهر را عوض کنیم
    city_id: Optional[int] = None
    is_active: Optional[bool] = None

class LawyerResponse(LawyerBase):
    id: int
    is_active: bool
    rating: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
