def setup(client):
    from telethon import events

    @client.on(events.NewMessage(pattern=r"\.start$", outgoing=True))
    async def start(event):
        await event.delete()
        await client.send_message(event.chat_id, "𝐁𝐎𝐋𝐎 𝐌𝐀𝐋𝐈𝐊 𝐊𝐈𝐒𝐊𝐎 𝐏𝐄𝐋𝐍𝐀 😈")