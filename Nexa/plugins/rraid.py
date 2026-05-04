def setup(client):
    from telethon import events
    import random
    from Nexa.sudo import is_sudo, is_fullsudo

    active = {}

    async def allowed(event):
        me = await client.get_me()
        return (
            event.sender_id == me.id
            or await is_fullsudo(me.id, event.sender_id)
            or await is_sudo(me.id, event.sender_id)
        )

    @client.on(events.NewMessage(pattern=r"\.rraid$"))
    async def rraid_on(event):
        if not await allowed(event):
            return

        if not event.is_reply:
            return await event.reply("Reply to user first")

        reply = await event.get_reply_message()

        active[event.chat_id] = reply.sender_id

        if event.out:
            await event.delete()

        await client.send_message(event.chat_id, "Reply Raid Active")

    @client.on(events.NewMessage(pattern=r"\.rrstop$"))
    async def rraid_off(event):
        if not await allowed(event):
            return

        active.pop(event.chat_id, None)

        if event.out:
            await event.delete()

        await client.send_message(event.chat_id, "Reply Raid Stopped")

    @client.on(events.NewMessage(incoming=True))
    async def watcher(event):
        if event.chat_id not in active:
            return

        if not event.is_reply:
            return

        try:
            reply = await event.get_reply_message()
        except:
            return

        target = active[event.chat_id]

        if reply.sender_id != target:
            return

        try:
            with open("word.txt", "r", encoding="utf-8") as f:
                words = [x.strip() for x in f.readlines() if x.strip()]
        except:
            return

        if not words:
            return

        word = random.choice(words)

        await event.reply(word)