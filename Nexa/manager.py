from telethon import TelegramClient
from telethon.sessions import StringSession
from Nexa.config import API_ID, API_HASH

clients = {}

async def start_client(user_id, string):
    if user_id in clients:
        return clients[user_id]

    client = TelegramClient(StringSession(string), API_ID, API_HASH)
    await client.start()

    clients[user_id] = client
    return client


async def stop_client(user_id):
    client = clients.get(user_id)
    if client:
        await client.disconnect()
        del clients[user_id]