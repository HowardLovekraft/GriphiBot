import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import InlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InputMessageContent
from Griphi.env.env_reader import get_token

router = Router()

@router.inline_query()
async def echo_inline(inline_query: InlineQuery):
    query_text = inline_query.query
    if not query_text:
        return
    results = []
    results.append(InlineQueryResultArticle(id='1',
                                            title='Echo',
                                            input_message_content=InputTextMessageContent(message_text=query_text)))

    await inline_query.answer(results=results, cache_time=1)
