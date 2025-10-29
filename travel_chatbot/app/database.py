import databases
from sqlalchemy import MetaData
from app.core.config import settings

database = databases.Database(settings.DATABASE_URL)
metadata = MetaData()

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()