from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from bot import app

CHANNELS = {
    "movies": "🎬 Movies",
    "anime": "🔥 Anime",
    "courses": "📚 Courses",
    "premium": "💎 Premium"
}

@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):

    buttons = []

    row = []

    for key, value in CHANNELS.items():

        row.append(
            InlineKeyboardButton(
                value,
                callback_data=f"channel_{key}"
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    await message.reply_text(
        "👋 Welcome\n\nChoose your channel:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
