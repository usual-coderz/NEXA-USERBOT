import asyncio
import json
import os
import importlib
from Nexa.manager import start_client
from Nexa.config import SESSIONS_FILE
from Nexa.bot import run_bot

def load_plugins(client):
    for file in os.listdir("Nexa/plugins"):
        if file.endswith(".py") and not file.startswith("__"):
            module = importlib.import_module(f"Nexa.plugins.{file[:-3]}")
            if hasattr(module, "setup"):
                module.setup(client)

async def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return

    with open(SESSIONS_FILE) as f:
        data = json.load(f)

    for user_id, string in data.items():
        try:
            client = await start_client(user_id, string)
            load_plugins(client)
        except:
            pass

async def main():
    await load_sessions()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run_bot)

    while True:
        await asyncio.sleep(999)

if __name__ == "__main__":
    asyncio.run(main())