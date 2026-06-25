# app/crud/location.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.location import Province, County, District, City

# ==================== Province CRUD ====================

async def create_province(db: AsyncSession, province_data: dict) -> Province:
    """ایجاد استان جدید"""
    db_province = Province(**province_data)
    db.add(db_province)
    await db.commit()
    await db.refresh(db_province)
    return db_province

async def get_province(db: AsyncSession, province_id: int) -> Optional[Province]:
    """دریافت استان بر اساس ID"""
    result = await db.execute(select(Province).where(Province.id == province_id))
    return result.scalar_one_or_none()

async def get_provinces(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Province]:
    """دریافت لیست استان‌ها"""
    result = await db.execute(select(Province).offset(skip).limit(limit))
    return result.scalars().all()

async def update_province(db: AsyncSession, db_province: Province, update_data: dict) -> Province:
    """بروزرسانی استان"""
    for key, value in update_data.items():
        setattr(db_province, key, value)
    await db.commit()
    await db.refresh(db_province)
    return db_province

async def delete_province(db: AsyncSession, province_id: int) -> bool:
    """حذف استان"""
    db_province = await get_province(db, province_id)
    if not db_province:
        return False
    await db.delete(db_province)
    await db.commit()
    return True

# ==================== County CRUD ====================

async def create_county(db: AsyncSession, county_data: dict) -> County:
    """ایجاد شهرستان جدید"""
    # بررسی تکراری نبودن
    existing = await get_county_by_name_and_province(
        db, county_data['name'], county_data['province_id']
    )
    if existing:
        raise ValueError(f"شهرستان '{county_data['name']}' در این استان قبلاً ثبت شده است")
    
    db_county = County(**county_data)
    db.add(db_county)
    await db.commit()
    await db.refresh(db_county)
    return db_county

async def get_county_by_name_and_province(db: AsyncSession, name: str, province_id: int) -> Optional[County]:
    """دریافت شهرستان بر اساس نام و استان"""
    result = await db.execute(
        select(County).where(County.name == name, County.province_id == province_id)
    )
    return result.scalar_one_or_none()

async def get_county(db: AsyncSession, county_id: int) -> Optional[County]:
    """دریافت شهرستان بر اساس ID"""
    result = await db.execute(select(County).where(County.id == county_id))
    return result.scalar_one_or_none()

async def get_counties(db: AsyncSession, skip: int = 0, limit: int = 100, province_id: Optional[int] = None) -> List[County]:
    """دریافت لیست شهرستان‌ها - با امکان فیلتر بر اساس استان"""
    query = select(County)
    if province_id:
        query = query.where(County.province_id == province_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def update_county(db: AsyncSession, db_county: County, update_data: dict) -> County:
    """بروزرسانی شهرستان"""
    for key, value in update_data.items():
        setattr(db_county, key, value)
    await db.commit()
    await db.refresh(db_county)
    return db_county

async def delete_county(db: AsyncSession, county_id: int) -> bool:
    """حذف شهرستان"""
    db_county = await get_county(db, county_id)
    if not db_county:
        return False
    await db.delete(db_county)
    await db.commit()
    return True

# ==================== District CRUD ====================

async def create_district(db: AsyncSession, district_data: dict) -> District:
    """ایجاد بخش جدید"""
    db_district = District(**district_data)
    db.add(db_district)
    await db.commit()
    await db.refresh(db_district)
    return db_district

async def get_district(db: AsyncSession, district_id: int) -> Optional[District]:
    """دریافت بخش بر اساس ID"""
    result = await db.execute(select(District).where(District.id == district_id))
    return result.scalar_one_or_none()

async def get_districts(db: AsyncSession, skip: int = 0, limit: int = 100, county_id: Optional[int] = None) -> List[District]:
    """دریافت لیست بخش‌ها - با امکان فیلتر بر اساس شهرستان"""
    query = select(District)
    if county_id:
        query = query.where(District.county_id == county_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def update_district(db: AsyncSession, db_district: District, update_data: dict) -> District:
    """بروزرسانی بخش"""
    for key, value in update_data.items():
        setattr(db_district, key, value)
    await db.commit()
    await db.refresh(db_district)
    return db_district

async def delete_district(db: AsyncSession, district_id: int) -> bool:
    """حذف بخش"""
    db_district = await get_district(db, district_id)
    if not db_district:
        return False
    await db.delete(db_district)
    await db.commit()
    return True

# ==================== City CRUD ====================

async def create_city(db: AsyncSession, city_data: dict) -> City:
    """ایجاد شهر جدید"""
    db_city = City(**city_data)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def get_city(db: AsyncSession, city_id: int) -> Optional[City]:
    """دریافت شهر بر اساس ID"""
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()

async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 100, district_id: Optional[int] = None) -> List[City]:
    """دریافت لیست شهرها - با امکان فیلتر بر اساس بخش"""
    query = select(City)
    if district_id:
        query = query.where(City.district_id == district_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def update_city(db: AsyncSession, db_city: City, update_data: dict) -> City:
    """بروزرسانی شهر"""
    for key, value in update_data.items():
        setattr(db_city, key, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int) -> bool:
    """حذف شهر"""
    db_city = await get_city(db, city_id)
    if not db_city:
        return False
    await db.delete(db_city)
    await db.commit()
    return True
