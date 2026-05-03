def setup(client):
    from telethon import events

    @client.on(events.NewMessage(pattern=r"\.start"))
    async def start(event):
        await event.reply("Nexa active")