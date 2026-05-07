from pyrogram.errors import UserNotParticipant
from config import MAIN_CHANNEL

async def is_user_joined(client, user_id):

    try:

        member = await client.get_chat_member(
            MAIN_CHANNEL,
            user_id
        )

        if member.status in [
            "member",
            "administrator",
            "owner"
        ]:
            return True

    except UserNotParticipant:
        return False

    except Exception:
        return False

    return False
