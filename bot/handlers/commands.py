from aiogram import Router, F, html
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(Command(commands="start"), F.chat.type == "private")
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Try (emoji at the end)", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="Try (emoji at the beginning)", switch_inline_query_current_chat=",")],
    ])
    await message.answer(
        "Hi! This bot allows you to send messages with different text emoji "
        f"(also known as {html.link(value='kaomoji', link='https://en.wikipedia.org/wiki/Emoticon#Japanese_style')}). "
        f"It works only via inline mode, and to try it, press any button below 👇\n\n"
        f"{html.italic('Note: to put kaomoji in front of your text, start your message with comma (,)')}\n\n"
        f"Source code is available {html.link(value='on GitHub', link='https://github.com/MasterGroosha/textfacesbot')}.",
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=kb
    )
