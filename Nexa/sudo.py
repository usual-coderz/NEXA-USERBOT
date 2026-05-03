from Nexa.database import db

col = db["sudo"]

async def add_sudo(user_id, target_id, level):
    await col.update_one(
        {"user_id": user_id, "target_id": target_id},
        {"$set": {"level": level}},
        upsert=True
    )

async def remove_sudo(user_id, target_id):
    await col.delete_one({"user_id": user_id, "target_id": target_id})

async def get_sudos(user_id):
    data = []
    async for doc in col.find({"user_id": user_id}):
        data.append(doc)
    return data

async def is_sudo(user_id, target_id):
    doc = await col.find_one({"user_id": user_id, "target_id": target_id})
    return doc

async def is_fullsudo(user_id, target_id):
    doc = await col.find_one({
        "user_id": user_id,
        "target_id": target_id,
        "level": "full"
    })
    return doc