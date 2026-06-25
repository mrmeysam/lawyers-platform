from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt  # <--- این خط بسیار مهم است (jwt اضافه شد)
from app.core.security import verify_password
from app.crud.admin import get_admin_by_username
from app.models.admin import Admin

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db(): 
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# تغییر به HTTPBearer
security = HTTPBearer()

async def authenticate_admin(db: AsyncSession, username: str, password: str) -> Admin:
    admin = await get_admin_by_username(db, username)
    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    
    # برای تست می‌توانید خط زیر را از کامنت خارج کنید تا توکن پرینت شود
    # print(f"Received Token: {token}")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = await get_admin_by_username(db, username=username)
    if admin is None:
        raise credentials_exception
    return admin
