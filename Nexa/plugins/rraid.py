def setup(client):
    from telethon import events
    import asyncio
    import random
    from Nexa.sudo import is_sudo, is_fullsudo

    active = {}
    tasks = {}

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
            return await event.reply("Reply to a user first")

        reply = await event.get_reply_message()
        chat_id = event.chat_id

        active[chat_id] = reply.sender_id

        if event.out:
            await event.delete()

        await client.send_message(chat_id, "Reply Raid Active")

    @client.on(events.NewMessage(pattern=r"\.rrstop$"))
    async def rraid_off(event):
        if not await allowed(event):
            return

        chat_id = event.chat_id

        active.pop(chat_id, None)

        if chat_id in tasks:
            tasks[chat_id].cancel()
            tasks.pop(chat_id, None)

        if event.out:
            await event.delete()

        await client.send_message(chat_id, "Reply Raid Stopped")

    @client.on(events.NewMessage)
    async def watcher(event):
        if event.chat_id not in active:
            return

        if not event.is_reply:
            return

        target = active[event.chat_id]

        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            if reply.sender_id != target:
                return

        try:
            with open("gali.txt", "r", encoding="utf-8") as f:
                words = [i.strip() for i in f.readlines() if i.strip()]
        except:
            return

        if not words:
            return

        word = random.choice(words)

        await client.send_message(
            event.chat_id,
            word,
            reply_to=event.id
        )