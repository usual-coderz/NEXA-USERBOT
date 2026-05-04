def setup(client):
    from telethon import events
    import time
    from Nexa.sudo import is_sudo, is_fullsudo

    async def allowed(event):
        me = await client.get_me()
        return (
            event.sender_id == me.id
            or await is_fullsudo(me.id, event.sender_id)
            or await is_sudo(me.id, event.sender_id)
        )

    @client.on(events.NewMessage(pattern=r"\.ping$"))
    async def ping(event):
        if not await allowed(event):
            return

        start = time.perf_counter()

        if event.out:
            await event.delete()

        msg = await client.send_message(event.chat_id, "Pinging...")

        ms = int((time.perf_counter() - start) * 1000)
        await msg.edit(f"𝐏𝐎𝐍𝐆 ⚡ {ms} 𝐦𝐬")