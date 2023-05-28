from pyrogram import Client, filters
from info import AUTH_CHANNEL, CHANNELS
from utils import temp
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video | filters.audio


@Client.on_chat_join_request()
async def ________(__, ___):
    if ___.chat.id == AUTH_CHANNEL:
        temp.REQUESTERS[___.chat.id] = {
            "list": temp.REQUESTERS.get(___.chat.id, {}).get("list", [])
            + [___.from_user.id],
            "date": temp.REQUESTERS.get(___.chat.id, {}).get("date", 0),
        }


@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    media.file_type = file_type
    media.caption = message.caption
    await save_file(media)