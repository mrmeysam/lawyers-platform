from sqlalchemy.ext.declarative import declarative_base

# Base مشترک برای تمام مدل‌ها
Base = declarative_base()

# ⚠️ بسیار مهم: حتماً باید همه مدل‌ها را اینجا ایمپورت کنیم تا دیتابیس آن‌ها را بشناسد
from app.models.admin import Admin
from app.models.lawyer import Lawyer
