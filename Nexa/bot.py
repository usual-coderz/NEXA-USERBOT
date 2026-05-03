import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from Nexa.config import API_ID, API_HASH, BOT_TOKEN, SESSIONS_FILE
from Nexa.manager import start_client
from Nexa.plugins import load as load_plugins

bot = TelegramClient("bot", API_ID, API_HASH)


def save_session(user_id, string):
    data = {}
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE) as f:
            data = json.load(f)

    data[str(user_id)] = string

    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Send /add <string_session>")


@bot.on(events.NewMessage(pattern=r"/add (.+)"))
async def add_session(event):
    user_id = event.sender_id
    string = event.pattern_match.group(1).strip()

    msg = await event.reply("Checking session...")

    try:
        test_client = TelegramClient(
            StringSession(string),
            API_ID,
            API_HASH
        )
        await test_client.connect()

        if not await test_client.is_user_authorized():
            await msg.edit("Invalid session")
            await test_client.disconnect()
            return

        me = await test_client.get_me()
        await test_client.disconnect()

        client = await start_client(user_id, string)
        load_plugins(client)

        save_session(user_id, string)

        await msg.edit(
            f"✅ Connected\n\n"
            f"👤 {me.first_name}\n"
            f"🆔 {me.id}"
        )

    except Exception as e:
        await msg.edit(f"Error: {str(e)[:100]}")


async def start_bot():
    await bot.start(bot_token=BOT_TOKEN)
    print("🤖 Control Bot Started")
    await bot.run_until_disconnected()