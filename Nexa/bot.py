from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

from Nexa.config import API_ID, API_HASH, BOT_TOKEN
from Nexa.manager import start_client, stop_client
from Nexa.plugins import load as load_plugins
from Nexa.utils.words import load_words
from Nexa.database import add_session, get_sessions, delete_session

bot = TelegramClient("bot", API_ID, API_HASH)

@bot.on(events.NewMessage(pattern=r"^/start$"))
async def start(event):
    buttons = [
        [Button.text("Add Session")],
        [Button.text("My Sessions")]
    ]
    await event.respond("Nexa Panel", buttons=buttons)

@bot.on(events.NewMessage(pattern=r"Add Session"))
async def ask_add(event):
    await event.reply("Send: /add <string_session>")

@bot.on(events.NewMessage(pattern=r"^/add\s+(.+)$"))
async def add(event):
    user_id = event.sender_id
    string = event.pattern_match.group(1).strip()
    msg = await event.reply("Checking...")

    try:
        test = TelegramClient(StringSession(string), API_ID, API_HASH)
        await test.connect()

        if not await test.is_user_authorized():
            await test.disconnect()
            return await msg.edit("Invalid session")

        me = await test.get_me()
        await test.disconnect()

        name = me.first_name or "User"

        session = await add_session(user_id, string, name)

        sid = str(session.inserted_id)

        client = await start_client(user_id, string, sid)
        load_plugins(client)

        await msg.edit(f"Connected: {name}")

    except Exception as e:
        await msg.edit(f"Error:\n{str(e)}")

@bot.on(events.NewMessage(pattern=r"My Sessions"))
async def list_sessions(event):
    user_id = event.sender_id
    data = await get_sessions(user_id)

    if not data:
        return await event.reply("No sessions")

    buttons = []
    text = "Your Sessions:\n\n"

    for d in data:
        sid = str(d["_id"])
        name = d.get("name", "User")

        text += f"• {name}\n"
        buttons.append([Button.inline(f"Remove {name}", data=f"del_{sid}")])

    await event.respond(text, buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b"del_(.*)"))
async def delete_cb(event):
    user_id = event.sender_id
    sid = event.data.decode().split("_")[1]

    await stop_client(user_id, sid)
    await delete_session(sid)

    await event.edit("Session removed")

async def start_bot():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot started")
    await bot.run_until_disconnected()