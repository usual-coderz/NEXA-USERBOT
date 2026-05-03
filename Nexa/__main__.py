import asyncio
from Nexa.manager import start_client
from Nexa.database import get_all_sessions
from Nexa.plugins import load as load_plugins
from Nexa.bot import start_bot

async def load_sessions():
    sessions = await get_all_sessions()

    for user_id, string in sessions:
        try:
            client = await start_client(user_id, string)
            load_plugins(client)
        except:
            pass

async def main():
    print("Starting Nexa")

    await load_sessions()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())