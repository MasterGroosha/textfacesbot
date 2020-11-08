import logging
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from os import getenv
from sys import exit

logging.basicConfig(level=logging.INFO)

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided. Terminated.")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

max_chars = 20      # How many chars to show in inline preview before cutting it with "..."
cache_time = 86400  # 1 day
faces = [line[:-1] for line in open("faces.txt", "rt", encoding="utf-8").readlines()]  # Loading text faces


def shorten(text):
    """
    If the `text` is longer than max_chars, it is cut and "..." symbols are added instead.
    :param text: Original text
    :return: Either original text or cut text with "..." symbol
    """
    stop_pos = max_chars if max_chars < len(text) else len(text)-1
    for i in range(stop_pos, -1, -1):
        if text[i] == " ":
            return text[:i] + "..."
    return text[:stop_pos]+"..."


@dp.inline_handler()  # Handle inline queries
async def inline_handler(query: types.InlineQuery):
    result_title = shorten(query.query) if len(query.query) > max_chars else query.query
    results = [
        types.InlineQueryResultArticle(
            id=str(index),
            title="{} {}".format(result_title if result_title else "", value),
            input_message_content=types.InputTextMessageContent(
                message_text="{}{}".format(query.query+" " if query.query else "", value)
            )

        ) for index, value in enumerate(faces)
    ]
    await query.answer(results=results, cache_time=cache_time)


@dp.message_handler()  # Handle regular messages
async def cmd_start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Press me :)", switch_inline_query=""))

    await message.answer("Hello there! Use this bot to send cool text smileys in any chat. "
                         "Press the button below to start. Have fun!", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
