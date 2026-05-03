def setup(client):
    from telethon import events
    from Nexa.sudo import is_sudo, is_fullsudo

    TEXT = "𝐁𝐎𝐋𝐎 𝐌𝐀𝐋𝐈𝐊 𝐊𝐈𝐒𝐊𝐎 𝐏𝐄𝐋𝐍𝐀 😈"

    async def allowed(event):
        me = await client.get_me()
        if event.sender_id == me.id:
            return True
        if await is_fullsudo(me.id, event.sender_id):
            return True
        if await is_sudo(me.id, event.sender_id):
            return True
        return False

    @client.on(events.NewMessage(pattern=r"\.start$", outgoing=True))
    async def start(event):
        if not await allowed(event):
            return
        await event.delete()
        await client.send_message(event.chat_id, TEXT)

    @client.on(events.NewMessage(outgoing=True))
    async def reply_name(event):
        if not await allowed(event):
            return

        if not event.is_reply:
            return

        reply = await event.get_reply_message()
        if not reply or reply.text != TEXT:
            return

        name = event.raw_text.strip()

        await event.delete()
        await client.send_message(event.chat_id, f"{name} 𝐕𝐎 𝐑𝐀𝐍𝐃𝐈 𝐔𝐒𝐊𝐈 𝐌𝐊𝐂 👺")