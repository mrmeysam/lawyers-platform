import os
import sys
from dotenv import load_dotenv  # ← اضافه
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.models import Base 
from app.models.lawyer import Lawyer
from app.models.admin import Admin



# ← این خط‌ها اضافه!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


target_metadata = Base.metadata

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError(f"DATABASE_URL not found! cwd: {os.getcwd()}")

config = context.config
config.set_main_option("sqlalchemy.url", database_url)

# بقیه همون...
def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # این خط را اضافه کنید یا اگر در تابع قبلی هست حفظ کنید
    # مطمئن شوید config تنظیم شده است
    config.set_main_option("sqlalchemy.url", database_url)
    
    asyncio.run(run_async_migrations())
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
