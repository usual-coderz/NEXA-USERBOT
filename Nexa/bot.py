import json
import os
from telethon import TelegramClient, events
from Nexa.config import API_ID, API_HASH, BOT_TOKEN, SESSIONS_FILE
from Nexa.manager import start_client

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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
    string = event.pattern_match.group(1)
    user_id = event.sender_id

    try:
        await start_client(user_id, string)
        save_session(user_id, string)
        await event.reply("Added")
    except Exception:
        await event.reply("Invalid session")

def run_bot():
    bot.run_until_disconnected()