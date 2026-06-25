from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
# LawyerCreate دیگر نیاز ندارد چون ثبت وکیل فقط توسط ادمین انجام می‌شود
from app.schemas.lawyer import LawyerResponse 
from app.crud import lawyer as crud_lawyer

router = APIRouter()

# متد POST حذف شد تا عموم نتوانند وکیل ثبت کنند.
# ثبت وکیل تنها از طریق بخش admin.py و با داشتن توکن امکان‌پذیر است.

@router.get("/{lawyer_id}", response_model=LawyerResponse)
async def read_lawyer(
    lawyer_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_lawyer = await crud_lawyer.get_lawyer(db=db, lawyer_id=lawyer_id)
    if db_lawyer is None:
        raise HTTPException(status_code=404, detail="وکیل یافت نشد")
    return db_lawyer

@router.get("/", response_model=List[LawyerResponse])
async def read_lawyers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    lawyers = await crud_lawyer.get_lawyers(db, skip=skip, limit=limit)
    return lawyers
