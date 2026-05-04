def setup(client):
    from telethon import events
    from Nexa.sudo import add_sudo, remove_sudo, get_sudos, is_sudo, is_fullsudo

    async def get_me_id():
        me = await client.get_me()
        return me.id

    @client.on(events.NewMessage(pattern=r"/addsudo$"))
    async def addsudo(event):
        if not event.is_reply:
            return await event.reply("Reply to user")

        me_id = await get_me_id()
        sender = event.sender_id

        if sender != me_id and not await is_fullsudo(me_id, sender):
            return

        reply = await event.get_reply_message()
        target = reply.sender_id

        await add_sudo(me_id, target, "sudo")
        await event.reply("Added Sudo")

    @client.on(events.NewMessage(pattern=r"/fullsudo$"))
    async def fullsudo(event):
        if not event.is_reply:
            return await event.reply("Reply to user")

        me_id = await get_me_id()
        sender = event.sender_id

        if sender != me_id:
            return

        reply = await event.get_reply_message()
        target = reply.sender_id

        await add_sudo(me_id, target, "full")
        await event.reply("Added Full Sudo")

    @client.on(events.NewMessage(pattern=r"/delsudo$"))
    async def delsudo(event):
        if not event.is_reply:
            return await event.reply("Reply to user")

        me_id = await get_me_id()
        sender = event.sender_id

        if sender != me_id and not await is_fullsudo(me_id, sender):
            return

        reply = await event.get_reply_message()
        target = reply.sender_id

        await remove_sudo(me_id, target)
        await event.reply("Removed")

    @client.on(events.NewMessage(pattern=r"/sudolist$"))
    async def sudolist(event):
        me = await client.get_me()
        me_id = me.id

        data = await get_sudos(me_id)

        if not data:
            return await event.reply("No sudo users")

        text = "Sudo Users:\n\n"

        for d in data:
            uid = d["target_id"]
            level = d["level"]

            try:
                user = await client.get_entity(uid)
                name = user.first_name or "User"
            except:
                name = "Unknown"

            text += f'<a href="tg://user?id={uid}">{name}</a> - {level}\n'

        await event.reply(text, parse_mode="html")