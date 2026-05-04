from telethon import events
import random
from Nexa.sudo import is_sudo, is_fullsudo
from Nexa.utils.words import load_words

active = {}

async def allowed(event, client):
    me = await client.get_me()
    return (
        event.sender_id == me.id
        or await is_fullsudo(me.id, event.sender_id)
        or await is_sudo(me.id, event.sender_id)
    )

def setup(client):

    @client.on(events.NewMessage(pattern=r"\.rraid$"))
    async def start(event):
        if not await allowed(event, client):
            return

        if not event.is_reply:
            return await event.reply("Reply to a user first")

        reply = await event.get_reply_message()
        active[event.chat_id] = reply.sender_id

        if event.out:
            await event.delete()

        await client.send_message(event.chat_id, "Reply Raid Active")

    @client.on(events.NewMessage(pattern=r"\.rrstop$"))
    async def stop(event):
        if not await allowed(event, client):
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

        reply = await event.get_reply_message()
        if not reply:
            return

        if reply.sender_id != active[event.chat_id]:
            return

        words = load_words()
        if not words:
            return

        word = random.choice(words)

        await client.send_message(
            event.chat_id,
            word,
            reply_to=event.id
        )