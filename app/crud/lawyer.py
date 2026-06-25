from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lawyer import Lawyer
from app.schemas.lawyer import LawyerCreate , LawyerUpdate

async def get_lawyer(db: AsyncSession, lawyer_id: int) -> Optional[Lawyer]:
    result = await db.execute(select(Lawyer).filter(Lawyer.id == lawyer_id))
    return result.scalar_one_or_none()

async def get_lawyer_by_phone(db: AsyncSession, phone: str) -> Optional[Lawyer]:
    result = await db.execute(select(Lawyer).filter(Lawyer.phone == phone))
    return result.scalar_one_or_none()

async def get_lawyers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Lawyer).offset(skip).limit(limit))
    return result.scalars().all()

async def create_lawyer(db: AsyncSession, lawyer: LawyerCreate) -> Lawyer:
    # ایجاد آبجکت مدل از داده‌های ورودی
    db_lawyer = Lawyer(
        full_name=lawyer.full_name,
        phone=lawyer.phone,
        license_number=lawyer.license_number,
        specialization=lawyer.specialization,
        city=lawyer.city,
        experience_years=lawyer.experience_years,
        # سایر فیلدها مثل rating و is_active مقدار پیش‌فرض مدل را می‌گیرند
    )
    db.add(db_lawyer)
    await db.commit()
    await db.refresh(db_lawyer)
    return db_lawyer

async def update_lawyer(db: AsyncSession, db_lawyer: Lawyer, lawyer_in: LawyerUpdate) -> Lawyer:
    update_data = lawyer_in.model_dump(exclude_unset=True) # فقط فیلدهایی که ارسال شده آپدیت شوند
    for field, value in update_data.items():
        setattr(db_lawyer, field, value)
    
    db.add(db_lawyer)
    await db.commit()
    await db.refresh(db_lawyer)
    return db_lawyer

async def delete_lawyer(db: AsyncSession, lawyer_id: int) -> Optional[Lawyer]:
    db_lawyer = await get_lawyer(db, lawyer_id)
    if db_lawyer:
        await db.delete(db_lawyer)
        await db.commit()
    return db_lawyer