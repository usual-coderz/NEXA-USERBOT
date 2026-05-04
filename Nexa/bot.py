from telethon import TelegramClient, events
from telethon.sessions import StringSession

from Nexa.config import API_ID, API_HASH, BOT_TOKEN
from Nexa.manager import start_client, clients
from Nexa.plugins import load as load_plugins
from Nexa.database import add_session

bot = TelegramClient("bot", API_ID, API_HASH)

@bot.on(events.NewMessage(pattern=r"^/start$"))
async def start(event):
    await event.reply("Send /add <string_session>")

@bot.on(events.NewMessage(pattern=r"^/add\s+(.+)$"))
async def add(event):
    user_id = event.sender_id
    string = event.pattern_match.group(1).strip()
    msg = await event.reply("Checking...")

    try:
        if user_id in clients:
            await msg.edit("Already connected")
            return

        test = TelegramClient(StringSession(string), API_ID, API_HASH)
        await test.connect()

        if not await test.is_user_authorized():
            await test.disconnect()
            await msg.edit("Invalid session")
            return

        me = await test.get_me()
        await test.disconnect()

        client = await start_client(user_id, string)
        load_plugins(client)

        await add_session(user_id, string)

        await msg.edit(f"Connected: {me.first_name}")

    except Exception as e:
        await msg.edit(f"Error:\n{str(e)}")

async def start_bot():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot started")
    await bot.run_until_disconnected()