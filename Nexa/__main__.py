import asyncio
from Nexa.bot import start_bot
from Nexa.manager import start_client
import json, os
from Nexa.config import SESSIONS_FILE

async def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return

    with open(SESSIONS_FILE) as f:
        data = json.load(f)

    for user_id, string in data.items():
        try:
            await start_client(user_id, string)
        except:
            pass

async def main():
    print("🔥 Starting Nexa System")

    await load_sessions()

    # 🔥 THIS LINE FIXES YOUR ISSUE
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())