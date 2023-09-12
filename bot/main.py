from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.misc import TgKeys
from bot.handlers import register_all_handlers

import logging
import openai

async def __on_start_up(dp: Dispatcher) -> None:
    openai.api_key = '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'

    logging.basicConfig(level=logging.INFO)
    register_all_handlers(dp)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)