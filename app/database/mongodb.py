from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]
organizations_collection = db["organizations"]

async def create_unique_email_index():
    await users_collection.create_index("email", unique=True)

async def init_db():
    await create_unique_email_index()
