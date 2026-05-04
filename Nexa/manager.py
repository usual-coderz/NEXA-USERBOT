from telethon import TelegramClient
from telethon.sessions import StringSession
from Nexa.config import API_ID, API_HASH

clients = {}

async def start_client(user_id, string, session_id):
    if not string:
        raise ValueError("Empty session string")

    client = TelegramClient(StringSession(string), API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        raise ValueError("Invalid or expired session")

    clients.setdefault(user_id, {})
    clients[user_id][session_id] = client

    return client


async def stop_client(user_id, session_id):
    if user_id in clients and session_id in clients[user_id]:
        await clients[user_id][session_id].disconnect()
        del clients[user_id][session_id]

        if not clients[user_id]:
            del clients[user_id]