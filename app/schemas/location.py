# app/schemas/location.py
from pydantic import BaseModel
from typing import Optional

# --- Province Schemas ---
class ProvinceBase(BaseModel):
    name: str

class ProvinceCreate(ProvinceBase):
    pass

class ProvinceUpdate(BaseModel):
    name: Optional[str] = None

class ProvinceResponse(ProvinceBase):
    id: int
    
    class Config:
        from_attributes = True

# --- County Schemas ---
class CountyBase(BaseModel):
    name: str
    province_id: int

class CountyCreate(CountyBase):
    pass

class CountyUpdate(BaseModel):
    name: Optional[str] = None
    province_id: Optional[int] = None

class CountyResponse(CountyBase):
    id: int
    
    class Config:
        from_attributes = True

# --- District Schemas ---
class DistrictBase(BaseModel):
    name: str
    county_id: int

class DistrictCreate(DistrictBase):
    pass

class DistrictUpdate(BaseModel):
    name: Optional[str] = None
    county_id: Optional[int] = None

class DistrictResponse(DistrictBase):
    id: int
    
    class Config:
        from_attributes = True

# --- City Schemas ---
class CityBase(BaseModel):
    name: str
    district_id: int

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: Optional[str] = None
    district_id: Optional[int] = None

class CityResponse(CityBase):
    id: int
    
    class Config:
        from_attributes = True
