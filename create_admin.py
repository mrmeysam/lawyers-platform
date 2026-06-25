import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.admin import Admin

# ساخت موتور اتصال به دیتابیس
engine = create_async_engine(settings.DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_super_admin():
    async with async_session() as session:
        async with session.begin():
            # بررسی اینکه آیا ادمین قبلا وجود دارد یا خیر
            result = await session.execute(
                select(Admin).where(Admin.username == "admin")
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print("Admin already exists!")
                return

            # ساخت ادمین جدید
            # username: admin
            # password: admin123
            new_admin = Admin(
                username="admin",
                hashed_password=get_password_hash("admin123")
            )
            session.add(new_admin)
            print("Admin user created successfully! (admin / admin123)")

if __name__ == "__main__":
    asyncio.run(create_super_admin())
