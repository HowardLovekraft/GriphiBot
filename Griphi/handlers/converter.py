import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.i18n import gettext as _

from main import bot
from speech.app import get_transcribe
from other.code_generator import generator
from other.info import BASE_DIR
from other.chat_type import ChatTypeFilter

router = Router()
i18n = I18n(path="locales", default_locale="en", domain="messages")
router.message.middleware(SimpleI18nMiddleware(i18n))
router.callback_query.middleware(SimpleI18nMiddleware(i18n))

async def get_file_id(message: Message) -> str | None:
    # we work only with voice/video_note and videos, so we have only 3 options of this function
    if message.voice is not None:
        return message.voice.file_id
    elif message.video_note is not None:
        return message.video_note.file_id
    elif message.video is not None:
        return message.video.file_id
    return None


async def work_media(message: Message, file_path) -> None:
    code = await generator()
    audio_file_name = f"{code}.mp3"
    path = f"{BASE_DIR}\\{audio_file_name}"

    await bot.download_file(file_path=file_path, destination=path, timeout=90, chunk_size=262144)
    reply_msg = await message.reply(text=_("I downloaded your file. Start transcribing..."))

    transcribe = await get_transcribe(audio_file_name)
    os.remove(path)
    await reply_msg.edit_text(text=transcribe)


@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(_("Hello, I'm Griphi.\nI can convert your voice messages and video notes to text.\n"
                           "To start, just forward to me a media file"))


@router.message((F.voice | F.video_note | F.video), ChatTypeFilter(["private"]))
async def get_media_dm(message: Message) -> None:
    file_id = await get_file_id(message)
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path

    await work_media(message, file_path)


@router.message(~(F.voice | F.video_note | F.video), ChatTypeFilter(["private"]))
async def get_not_media_dm(message: Message) -> None:
    await message.reply(_("Please, send me only:\n- voice messages\n- video notes\n- videos"))


@router.message((F.text.lower() == "griphi"), ChatTypeFilter(["group", "supergroup"]))
async def get_media_group(message: Message) -> None:
    replied_msg = message.reply_to_message
    if replied_msg is not None:
        file_id = await get_file_id(replied_msg)
        if file_id is not None:
            file = await bot.get_file(file_id=file_id)
            file_path = file.file_path

            await work_media(replied_msg, file_path)
        else:
            await message.reply("Please, dm me in reply of a *media* file",
                                parse_mode="MarkdownV2")
    else:
        await message.reply("Please, dm me in *reply* of a media file",
                            parse_mode="MarkdownV2")
