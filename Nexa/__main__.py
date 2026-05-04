import asyncio
from Nexa.manager import start_client
from Nexa.database import get_all_sessions
from Nexa.plugins import load as load_plugins
from Nexa.bot import start_bot

async def load_sessions():
    sessions = await get_all_sessions()

    for doc in sessions:
        try:
            user_id = doc["user_id"]
            string = doc["string"]
            session_id = str(doc["_id"])

            client = await start_client(user_id, string, session_id)
            load_plugins(client)

        except Exception as e:
            print("SESSION LOAD ERROR:", e)

async def main():
    print("Starting Nexa")

    await load_sessions()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())