def setup(client):
    from telethon import events

    @client.on(events.NewMessage(pattern=r"\.start$", outgoing=True))
    async def start(event):
        await event.delete()
        await client.send_message(event.chat_id, "Nexa active")