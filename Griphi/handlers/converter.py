import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.i18n import gettext as _
from aiogram.methods.get_file import GetFile

from Griphi.env.env_reader import get_token
from Griphi.speech.app import get_transcribe
from Griphi.other.code_generator import generator


bot = Bot(token=get_token())
router = Router()
i18n = I18n(path="locales", default_locale="en", domain="messages")
router.message.middleware(SimpleI18nMiddleware(i18n))

@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(_("Hello, I'm Griphi.\nI can convert your voice messages to text"))


@router.message(F.voice)
async def echo_inline(message: Message):
    file_id = message.voice.file_id
    file = await GetFile(file_id=file_id)
    file_path = file.file_path
    code = await generator()

    path = f"C:\\GitHub\\GriphiBot\\Griphi\\speech\\{code}.mp3"
    await bot.download_file(file_path=file_path,
                            destination=path)
    await message.reply(text=_("I got ur voice message. Please, wait..."))

    audio_file_name = f"{code}.mp3"
    transcribe = await get_transcribe(audio_file_name)
    os.remove(path)
    await message.answer(text=transcribe)
