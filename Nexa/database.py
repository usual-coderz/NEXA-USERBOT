from motor.motor_asyncio import AsyncIOMotorClient
from Nexa.config import MONGO_URI, DB_NAME, COLLECTION

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo[DB_NAME]
col = db[COLLECTION]


async def add_session(user_id, string):
    await col.update_one(
        {"user_id": user_id},
        {"$set": {"string": string}},
        upsert=True
    )


async def get_all_sessions():
    data = []
    async for doc in col.find():
        data.append((doc["user_id"], doc["string"]))
    return data


async def delete_session(user_id):
    await col.delete_one({"user_id": user_id})