from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from bot import app
from plugins.force_sub import is_user_joined
from config import MAIN_CHANNEL

CHANNELS = {
    "movies": {
        "name": "🎬 Movies",
        "chat_id": -1001111111111
    },

    "anime": {
        "name": "🔥 Anime",
        "chat_id": -1002222222222
    },

    "courses": {
        "name": "📚 Courses",
        "chat_id": -1003333333333
    },

    "premium": {
        "name": "💎 Premium",
        "chat_id": -1004444444444
    }
}

@app.on_callback_query(filters.regex("^channel_"))
async def channel_callback(client, callback_query):

    user_id = callback_query.from_user.id

    channel_key = callback_query.data.split("_")[1]

    joined = await is_user_joined(client, user_id)

    if not joined:

        buttons = [
            [
                InlineKeyboardButton(
                    "📢 Join Main Channel",
                    url=f"https://t.me/{MAIN_CHANNEL.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 Retry",
                    callback_data=f"retry_{channel_key}"
                )
            ]
        ]

        return await callback_query.message.edit_text(
            "❌ Join main channel first.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    channel_data = CHANNELS[channel_key]

    expire_time = datetime.now() + timedelta(minutes=5)

    invite_link = await client.create_chat_invite_link(
        chat_id=channel_data["chat_id"],
        expire_date=expire_time,
        member_limit=1
    )

    await callback_query.message.edit_text(
        f"✅ Access Granted\n\n"
        f"{invite_link.invite_link}"
    )

@app.on_callback_query(filters.regex("^retry_"))
async def retry_callback(client, callback_query):

    channel_key = callback_query.data.split("_")[1]

    joined = await is_user_joined(
        client,
        callback_query.from_user.id
    )

    if not joined:
        return await callback_query.answer(
            "Still not joined.",
            show_alert=True
        )

    channel_data = CHANNELS[channel_key]

    expire_time = datetime.now() + timedelta(minutes=5)

    invite_link = await client.create_chat_invite_link(
        chat_id=channel_data["chat_id"],
        expire_date=expire_time,
        member_limit=1
    )

    await callback_query.message.edit_text(
        f"✅ Verified\n\n"
        f"{invite_link.invite_link}"
    )
