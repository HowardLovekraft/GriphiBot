import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.i18n import gettext as _
from aiogram.methods.get_file import GetFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from env.env_reader import get_token
from speech.app import get_transcribe
from other.code_generator import generator
from other.info import BASE_DIR
from keyboards.queue_kb import get_accept

bot = Bot(token=get_token())
router = Router()
i18n = I18n(path="locales", default_locale="en", domain="messages")
router.message.middleware(SimpleI18nMiddleware(i18n))
router.callback_query.middleware(SimpleI18nMiddleware(i18n))


class Transcriber(StatesGroup):
    work_media = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(_("Hello, I'm Griphi.\nI can convert your voice messages and video notes to text.\n"
                           "To start, just forward to me a media file"))


@router.message(F.voice)
async def get_voice(message: Message, state: FSMContext) -> None:
    file_id = message.voice.file_id
    file = await GetFile(file_id=file_id)

    data = await state.get_data()
    data["file"] = file.file_path
    await state.set_data(data)

    await message.reply(text=_("I got ur voice message. Do u want to start transcribing?"),
                        reply_markup=get_accept())
    await state.set_state(Transcriber.work_media)

@router.message(F.video_note)
async def get_video_note(message: Message, state: FSMContext) -> None:
    file_id = message.video_note.file_id
    file = await GetFile(file_id=file_id)

    data = await state.get_data()
    data["file"] = file.file_path
    await state.set_data(data)
    await message.reply(text=_("I got ur video note. Do u want to start transcribing?"),
                        reply_markup=get_accept())
    await state.set_state(Transcriber.work_media)


@router.message(F.video)
async def get_video_file(message: Message, state: FSMContext) -> None:
    file_id = message.video.file_id
    file = await GetFile(file_id=file_id)

    data = await state.get_data()
    data["file"] = file.file_path
    await state.set_data(data)
    await message.reply(text="I got ur video file. Do u want to start transcribing?",
                        reply_markup=get_accept())
    await state.set_state(Transcriber.work_media)

@router.message(~(F.voice | F.video_note| F.video))
async def get_not_media(message: Message) -> None:
    await message.reply(_("Please, send me only voice messages/video notes"))

@router.callback_query(Transcriber.work_media)
async def work_media(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "accept":
        await callback.answer()
        await callback.message.edit_text(_("Please wait..."))

        code = await generator()
        path = f"{BASE_DIR}\\{code}.mp3"
        audio_file_name = f"{code}.mp3"

        data = await state.get_data()
        await bot.download_file(file_path=data["file"],
                                destination=path,
                                timeout=90,
                                chunk_size=262144)
        await callback.message.edit_text(text=_("I downloaded your file. Start transcribing..."))

        transcribe = await get_transcribe(audio_file_name)
        os.remove(path)

        await callback.message.edit_text(text=transcribe)

    elif callback.data == "cancel":
        await callback.answer()
        await callback.message.edit_text(_("You canceled the process"))

    await state.clear()
