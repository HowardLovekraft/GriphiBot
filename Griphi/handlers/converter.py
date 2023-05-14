import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.i18n import gettext as _
from aiogram.methods.get_file import GetFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from Griphi.env.env_reader import get_token
from Griphi.speech.app import get_transcribe
from Griphi.other.code_generator import generator
from Griphi.other.info import BASE_DIR
from Griphi.keyboards.queue_kb import get_accept

bot = Bot(token=get_token())
router = Router()
i18n = I18n(path="locales", default_locale="en", domain="messages")
router.message.middleware(SimpleI18nMiddleware(i18n))
router.callback_query.middleware(SimpleI18nMiddleware(i18n))


class Transcriber(StatesGroup):
    get_voice = State()
    work_voice = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(_("Hello, I'm Griphi.\nI can convert your voice messages to text"))
    await state.set_state(Transcriber.get_voice)


@router.message(F.voice, Transcriber.get_voice)
async def echo_inline(message: Message, state: FSMContext) -> None:
    file_id = message.voice.file_id
    file = await GetFile(file_id=file_id)

    data = await state.get_data()
    data["file"] = file.file_path
    await state.set_data(data)

    await message.reply(text=_("I got ur voice message. Do u want to start transcribing?"),
                        reply_markup=get_accept())
    await state.set_state(Transcriber.work_voice)

@router.callback_query(Transcriber.work_voice)
async def work_voice(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "accept":
        await callback.answer()
        await callback.message.edit_text(_("Please wait..."))

        code = await generator()
        path = f"{BASE_DIR}\\{code}.mp3"
        audio_file_name = f"{code}.mp3"

        data = await state.get_data()
        await bot.download_file(file_path=data["file"],
                                destination=path)

        transcribe = await get_transcribe(audio_file_name)
        os.remove(path)

        await callback.message.edit_text(text=transcribe)

    elif callback.data == "cancel":
        await callback.answer()
        await callback.message.edit_text(_("You canceled the process"))

    await state.clear()
    await state.set_state(Transcriber.get_voice)
