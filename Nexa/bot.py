from telethon import TelegramClient, events
from Nexa.config import API_ID, API_HASH, BOT_TOKEN

bot = TelegramClient("bot", API_ID, API_HASH)

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Bot working ✅")

async def start_bot():
    await bot.start(bot_token=BOT_TOKEN)
    print("🤖 Control Bot Started")
    await bot.run_until_disconnected()