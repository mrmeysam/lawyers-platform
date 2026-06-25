# app/api/v1/endpoints/admin.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_admin # <-- ایمپورت ادمین فعلی
from app.schemas.lawyer import LawyerCreate, LawyerUpdate, LawyerResponse
from app.crud import lawyer as crud_lawyer
from app.models.admin import Admin # <--- ایمپورت مدل ادمین

router = APIRouter()

# تمام توابع باید پارامتر current_admin: Admin = Depends(get_current_admin) را داشته باشند

@router.post("/", response_model=LawyerResponse)
async def admin_create_lawyer(
    lawyer: LawyerCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin) # <--- محافظت شده
):
    existing = await crud_lawyer.get_lawyer_by_phone(db, phone=lawyer.phone)
    if existing:
        raise HTTPException(status_code=400, detail="شماره تماس قبلاً ثبت شده است")

    return await crud_lawyer.create_lawyer(db=db, lawyer=lawyer)

@router.get("/", response_model=List[LawyerResponse])
async def admin_list_lawyers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin) # <--- محافظت شده
):
    lawyers = await crud_lawyer.get_lawyers(db, skip=skip, limit=limit)
    return lawyers

@router.get("/{lawyer_id}", response_model=LawyerResponse)
async def admin_get_lawyer(
    lawyer_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin) # <--- محافظت شده
):
    db_lawyer = await crud_lawyer.get_lawyer(db=db, lawyer_id=lawyer_id)
    if db_lawyer is None:
        raise HTTPException(status_code=404, detail="وکیل یافت نشد")
    return db_lawyer

@router.put("/{lawyer_id}", response_model=LawyerResponse)
async def admin_update_lawyer(
    lawyer_id: int,
    lawyer_update: LawyerUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin) # <--- محافظت شده
):
    db_lawyer = await crud_lawyer.get_lawyer(db=db, lawyer_id=lawyer_id)
    if db_lawyer is None:
        raise HTTPException(status_code=404, detail="وکیل یافت نشد")

    return await crud_lawyer.update_lawyer(db=db, db_lawyer=db_lawyer, lawyer_in=lawyer_update)

@router.delete("/{lawyer_id}")
async def admin_delete_lawyer(
    lawyer_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin) # <--- محافظت شده
):
    db_lawyer = await crud_lawyer.delete_lawyer(db=db, lawyer_id=lawyer_id)
    if db_lawyer is None:
        raise HTTPException(status_code=404, detail="وکیل یافت نشد")
    return {"message": "وکیل با موفقیت حذف شد"}
