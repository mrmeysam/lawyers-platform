from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ⚠️ تغییر مهم اینجاست: از routers به router تغییر دادیم
from app.api.v1 import router 

from app.core.config import settings

app = FastAPI(
    title="لیست وکلا API",
    description="API بک‌اند لیست وکلا",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
# ⚠️ این خط را هم اصلاح کنید:
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "لیست وکلا API 🚀"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
