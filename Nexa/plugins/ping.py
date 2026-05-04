def setup(client):
    from telethon import events
    import time
    from Nexa.sudo import is_sudo, is_fullsudo

    async def allowed(event):
        me = await client.get_me()
        if event.sender_id == me.id:
            return True
        if await is_fullsudo(me.id, event.sender_id):
            return True
        if await is_sudo(me.id, event.sender_id):
            return True
        return False

    @client.on(events.NewMessage(pattern=r"\.ping$"))
    async def ping(event):
        if not await allowed(event):
            return

        start = time.time()

        if event.out:
            await event.delete()

        msg = await client.send_message(event.chat_id, "Pinging...")

        end = time.time()
        ms = round((end - start) * 1000)

        await msg.edit(f"𝐏𝐎𝐍𝐆 ⚡ {ms} 𝐦𝐬")