from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n import gettext as _

i18n = I18n(path="locales", default_locale="en", domain="messages")

def get_accept() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text=_("Accept"),
              callback_data="accept")
    ikb.button(text=_("Cancel"),
              callback_data="cancel")
    ikb.adjust(2)
    return ikb.as_markup()
