def setup(client):
    from telethon import events
    import asyncio
    from Nexa.sudo import is_sudo, is_fullsudo

    raid_tasks = {}

    async def allowed(event):
        me = await client.get_me()
        return (
            event.sender_id == me.id
            or await is_fullsudo(me.id, event.sender_id)
            or await is_sudo(me.id, event.sender_id)
        )

    @client.on(events.NewMessage(pattern=r"\.raid\s+(.+)$"))
    async def raid(event):
        if not await allowed(event):
            return

        args = event.pattern_match.group(1).strip().split()

        if len(args) < 2:
            return await event.reply("Usage: .raid <user/msg> <msg> <count>")

        count = int(args[-1])
        count = max(1, min(count, 500))

        target = None

        if event.is_reply:
            reply = await event.get_reply_message()
            target = reply.sender_id
            msg_text = " ".join(args[:-1])
        else:
            first = args[0]
            try:
                if first.isdigit():
                    target = int(first)
                    msg_text = " ".join(args[1:-1])
                else:
                    user = await client.get_entity(first)
                    target = user.id
                    msg_text = " ".join(args[1:-1])
            except:
                return await event.reply("Invalid user")

        try:
            user = await client.get_entity(target)
            name = user.first_name or "User"
        except:
            name = "User"

        mention = f'<a href="tg://user?id={target}">{name}</a>'

        if event.out:
            await event.delete()

        async def spam():
            for _ in range(count):
                if event.chat_id not in raid_tasks:
                    break
                await client.send_message(
                    event.chat_id,
                    f"{mention} {msg_text}",
                    parse_mode="html"
                )
                await asyncio.sleep(1)

            raid_tasks.pop(event.chat_id, None)

        task = asyncio.create_task(spam())
        raid_tasks[event.chat_id] = task

    @client.on(events.NewMessage(pattern=r"\.stopraid$"))
    async def stopraid(event):
        if not await allowed(event):
            return

        if event.chat_id in raid_tasks:
            raid_tasks[event.chat_id].cancel()
            raid_tasks.pop(event.chat_id, None)

            if event.out:
                await event.delete()

            await client.send_message(event.chat_id, "Raid stopped")
        else:
            await event.reply("No active raid")