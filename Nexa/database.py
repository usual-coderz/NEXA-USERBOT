from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from Nexa.config import MONGO_URI, DB_NAME, COLLECTION

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo[DB_NAME]
col = db[COLLECTION]


async def add_session(user_id, string, name):
    result = await col.insert_one({
        "user_id": user_id,
        "string": string,
        "name": name
    })
    return result


async def get_sessions(user_id):
    data = []
    async for doc in col.find({"user_id": user_id}):
        data.append(doc)
    return data


async def get_all_sessions():
    data = []
    async for doc in col.find():
        data.append(doc)
    return data


async def delete_session(session_id):
    await col.delete_one({"_id": ObjectId(session_id)})