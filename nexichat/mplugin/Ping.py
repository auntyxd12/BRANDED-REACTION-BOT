import asyncio
import logging
import random
import time
import psutil
import config
import os
from nexichat import _boot_
from nexichat import get_readable_time
from nexichat.mplugin.helpers import is_owner
from nexichat import nexichat
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from nexichat import db
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from nexichat.database.chats import get_served_chats, add_served_chat
from nexichat.database.users import get_served_users, add_served_user
from nexichat.database.clonestats import get_served_cchats, get_served_cusers, add_served_cuser, add_served_cchat
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from nexichat.mplugin.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
)

IMG = [
    "https://files.catbox.moe/t57fdb.jpg",
    "https://files.catbox.moe/g41f9e.jpg",
    "https://files.catbox.moe/c9hkff.jpg",
    "https://files.catbox.moe/0kpdw9.jpg",
    "https://files.catbox.moe/6xiocz.jpg",
    "https://files.catbox.moe/dz22a1.jpg",
    "https://files.catbox.moe/9iwpfv.jpg",
    "https://files.catbox.moe/3mvh25.jpg",
    "https://files.catbox.moe/nzpm5w.jpg",
    "https://files.catbox.moe/mjez4q.jpg",
    "https://files.catbox.moe/h75qko.jpg",
    "https://files.catbox.moe/68hu5w.jpg",
    "https://files.catbox.moe/rkdx6x.jpg",
    "https://files.catbox.moe/bv1ky8.jpg",
]


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK


@Client.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    bot_id = client.me.id
    start = datetime.now()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    loda = await message.reply_photo(
        photo=random.choice(IMG),
        caption="ᴘɪɴɢɪɴɢ...",
    )

    ms = (datetime.now() - start).microseconds / 1000
    await loda.edit_text(
        text=f"нey вαву!!\n{(await client.get_me()).mention} ᴄʜᴀᴛʙᴏᴛ ιѕ alιve 🥀 αnd worĸιng ғιne wιтн a pιng oғ\n\n**➥** `{ms}` ms\n**➲ ᴄᴘᴜ:** {CPU}\n**➲ ʀᴀᴍ:** {RAM}\n**➲ ᴅɪsᴋ:** {DISK}\n**➲ ᴜᴘᴛɪᴍᴇ »** {UP}\n\n<b>||**๏ мαdє ωιтн ❣️ ву [˹ʟᴇɢᴇɴᴅ-ᴍɪᴄᴋᴇʏ˼](https://t.me/{OWNER_USERNAME}) **||</b>",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )
    if message.chat.type == ChatType.PRIVATE:
        await add_served_cuser(bot_id, message.from_user.id)
        await add_served_user(message.from_user.id)
    else:
        await add_served_cchat(bot_id, message.chat.id)
        await add_served_chat(message.chat.id)
