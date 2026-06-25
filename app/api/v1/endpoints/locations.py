# app/api/v1/endpoints/locations.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.api.dependencies import get_db, get_current_admin
from app.schemas.location import (
    ProvinceCreate, ProvinceUpdate, ProvinceResponse,
    CountyCreate, CountyUpdate, CountyResponse,
    DistrictCreate, DistrictUpdate, DistrictResponse,
    CityCreate, CityUpdate, CityResponse
)
from app.crud import location as crud_location
from app.models.admin import Admin

router = APIRouter()

# ==================== Province Endpoints ====================

@router.post("/provinces", response_model=ProvinceResponse, summary="ایجاد استان جدید")
async def create_province(
    province: ProvinceCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """ایجاد یک استان جدید (نیاز به احراز هویت ادمین)"""
    return await crud_location.create_province(db, province.model_dump())

@router.get("/provinces", response_model=List[ProvinceResponse], summary="دریافت لیست استان‌ها")
async def list_provinces(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت لیست تمام استان‌ها با صفحه‌بندی"""
    return await crud_location.get_provinces(db, skip, limit)

@router.get("/provinces/{province_id}", response_model=ProvinceResponse, summary="دریافت استان بر اساس ID")
async def get_province(
    province_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت اطلاعات یک استان خاص"""
    province = await crud_location.get_province(db, province_id)
    if not province:
        raise HTTPException(status_code=404, detail="استان یافت نشد")
    return province

@router.put("/provinces/{province_id}", response_model=ProvinceResponse, summary="بروزرسانی استان")
async def update_province(
    province_id: int,
    province: ProvinceUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """بروزرسانی اطلاعات یک استان"""
    db_province = await crud_location.get_province(db, province_id)
    if not db_province:
        raise HTTPException(status_code=404, detail="استان یافت نشد")
    return await crud_location.update_province(db, db_province, province.model_dump(exclude_unset=True))

@router.delete("/provinces/{province_id}", summary="حذف استان")
async def delete_province(
    province_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """حذف یک استان (همراه با تمام شهرستان‌ها، بخش‌ها و شهرهای زیرمجموعه)"""
    if not await crud_location.delete_province(db, province_id):
        raise HTTPException(status_code=404, detail="استان یافت نشد")
    return {"message": "استان با موفقیت حذف شد"}

# ==================== County Endpoints ====================

@router.post("/counties", response_model=CountyResponse, summary="ایجاد شهرستان جدید")
async def create_county(
    county: CountyCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """ایجاد یک شهرستان جدید (نیاز به احراز هویت ادمین)"""
    try:
        return await crud_location.create_county(db, county.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/counties", response_model=List[CountyResponse], summary="دریافت لیست شهرستان‌ها")
async def list_counties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    province_id: Optional[int] = Query(None, description="فیلتر بر اساس ID استان"),
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت لیست شهرستان‌ها با امکان فیلتر بر اساس استان"""
    return await crud_location.get_counties(db, skip, limit, province_id)

@router.get("/counties/{county_id}", response_model=CountyResponse, summary="دریافت شهرستان بر اساس ID")
async def get_county(
    county_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت اطلاعات یک شهرستان خاص"""
    county = await crud_location.get_county(db, county_id)
    if not county:
        raise HTTPException(status_code=404, detail="شهرستان یافت نشد")
    return county

@router.put("/counties/{county_id}", response_model=CountyResponse, summary="بروزرسانی شهرستان")
async def update_county(
    county_id: int,
    county: CountyUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """بروزرسانی اطلاعات یک شهرستان"""
    db_county = await crud_location.get_county(db, county_id)
    if not db_county:
        raise HTTPException(status_code=404, detail="شهرستان یافت نشد")
    return await crud_location.update_county(db, db_county, county.model_dump(exclude_unset=True))

@router.delete("/counties/{county_id}", summary="حذف شهرستان")
async def delete_county(
    county_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """حذف یک شهرستان (همراه با تمام بخش‌ها و شهرهای زیرمجموعه)"""
    if not await crud_location.delete_county(db, county_id):
        raise HTTPException(status_code=404, detail="شهرستان یافت نشد")
    return {"message": "شهرستان با موفقیت حذف شد"}

# ==================== District Endpoints ====================

@router.post("/districts", response_model=DistrictResponse, summary="ایجاد بخش جدید")
async def create_district(
    district: DistrictCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """ایجاد یک بخش جدید"""
    return await crud_location.create_district(db, district.model_dump())

@router.get("/districts", response_model=List[DistrictResponse], summary="دریافت لیست بخش‌ها")
async def list_districts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    county_id: Optional[int] = Query(None, description="فیلتر بر اساس ID شهرستان"),
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت لیست بخش‌ها با امکان فیلتر بر اساس شهرستان"""
    return await crud_location.get_districts(db, skip, limit, county_id)

@router.get("/districts/{district_id}", response_model=DistrictResponse, summary="دریافت بخش بر اساس ID")
async def get_district(
    district_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت اطلاعات یک بخش خاص"""
    district = await crud_location.get_district(db, district_id)
    if not district:
        raise HTTPException(status_code=404, detail="بخش یافت نشد")
    return district

@router.put("/districts/{district_id}", response_model=DistrictResponse, summary="بروزرسانی بخش")
async def update_district(
    district_id: int,
    district: DistrictUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """بروزرسانی اطلاعات یک بخش"""
    db_district = await crud_location.get_district(db, district_id)
    if not db_district:
        raise HTTPException(status_code=404, detail="بخش یافت نشد")
    return await crud_location.update_district(db, db_district, district.model_dump(exclude_unset=True))

@router.delete("/districts/{district_id}", summary="حذف بخش")
async def delete_district(
    district_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """حذف یک بخش (همراه با تمام شهرهای زیرمجموعه)"""
    if not await crud_location.delete_district(db, district_id):
        raise HTTPException(status_code=404, detail="بخش یافت نشد")
    return {"message": "بخش با موفقیت حذف شد"}

# ==================== City Endpoints ====================

@router.post("/cities", response_model=CityResponse, summary="ایجاد شهر جدید")
async def create_city(
    city: CityCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """ایجاد یک شهر جدید"""
    return await crud_location.create_city(db, city.model_dump())

@router.get("/cities", response_model=List[CityResponse], summary="دریافت لیست شهرها")
async def list_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    district_id: Optional[int] = Query(None, description="فیلتر بر اساس ID بخش"),
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت لیست شهرها با امکان فیلتر بر اساس بخش"""
    return await crud_location.get_cities(db, skip, limit, district_id)

@router.get("/cities/{city_id}", response_model=CityResponse, summary="دریافت شهر بر اساس ID")
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """دریافت اطلاعات یک شهر خاص"""
    city = await crud_location.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="شهر یافت نشد")
    return city

@router.put("/cities/{city_id}", response_model=CityResponse, summary="بروزرسانی شهر")
async def update_city(
    city_id: int,
    city: CityUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """بروزرسانی اطلاعات یک شهر"""
    db_city = await crud_location.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="شهر یافت نشد")
    return await crud_location.update_city(db, db_city, city.model_dump(exclude_unset=True))

@router.delete("/cities/{city_id}", summary="حذف شهر")
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """حذف یک شهر"""
    if not await crud_location.delete_city(db, city_id):
        raise HTTPException(status_code=404, detail="شهر یافت نشد")
    return {"message": "شهر با موفقیت حذف شد"}
