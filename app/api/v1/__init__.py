from fastapi import APIRouter
from app.api.v1.endpoints import lawyers, admin, auth ,locations

router = APIRouter()

# مسیرهای عمومی
router.include_router(lawyers.router, tags=["Public - Lawyers"])

# مسیرهای احراز هویت (بدون پیشوند خاص، یا با /auth)
router.include_router(auth.router, tags=["Authentication"])

# مسیرهای ادمین (همانطور که بود)
router.include_router(admin.router, prefix="/admin", tags=["Admin lawyers"])

router.include_router(locations.router, prefix="/admin/locations", tags=["Admin locations"])
