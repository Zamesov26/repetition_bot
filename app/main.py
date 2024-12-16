import asyncio
import logging
import sqlite3
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.formatting import Text, Spoiler

from app.keyboard import note_message

TOKEN = getenv("TOKEN")
DB_PATH = getenv("DB")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(
    message: Message
) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


def get_note():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    data = cur.execute(NOTE_QUERY).fetchone()
    if data:
        id_, name, description, more, example = data
        message_data = note_message(id_, name, description, more=more, example=example)
    else:
        message_data = {"text": "для вас пока нету сообщения"}
    con.close()
    return message_data


@dp.callback_query(F.data.startswith('note:ok:'))
async def some_callback(
    call: CallbackQuery
) -> None:
    *_, id_ = call.data.split(':')
    await bot.send_message(
        chat_id=call.from_user.id,
        **get_note()
    )
    await call.message.delete()


@dp.message()
async def echo_handler(
    message: Message
) -> None:
    # if False:
    #     # TODO: только для меня
    #     return
    await message.answer(**get_note())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
