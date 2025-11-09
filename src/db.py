from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config
client = None
db = None
def init_db():
    global client, db
    if not Config.MONGO_URI:
        return None
    client = AsyncIOMotorClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]
    return db
async def ensure_user(collection, user):
    if not collection:
        return
    await collection.update_one(
        {"id": user.id},
        {"$setOnInsert": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "added_on": __import__('datetime').datetime.utcnow()
        }},
        upsert=True
    )
