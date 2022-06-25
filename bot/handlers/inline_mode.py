from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from bot.middlewares import FacesMiddleware
from bot.misc import get_faces

router = Router()
router.inline_query.middleware(FacesMiddleware(get_faces()))

max_chars = 20  # How many chars to show in inline preview before cutting it with "..."
cache_time = 3600 * 6  # 6 hours


def shorten(text: str) -> str:
    """
    Cuts the text to no more than max_chars symbols
    :param text: original text
    :return: Cut text which has no more than max_chars symbols
    """
    for i in range(max_chars, -1, -1):
        if text[i] == " ":
            return f"{text[:i]}…"
    # If no space was found, just cut it "as is"
    return f"{text[:max_chars]}…"


@router.inline_query(F.query == "")
@router.inline_query(F.query == ",")
async def empty_inline_query(inline_query: InlineQuery, faces: list[str]):
    results = [
        InlineQueryResultArticle(
            id=str(index),
            title=f"{value}",
            input_message_content=InputTextMessageContent(
                message_text=value
            )
        ) for index, value in enumerate(faces)
    ]
    await inline_query.answer(
        results=results, cache_time=cache_time,
        switch_pm_text="Help and source code", switch_pm_parameter="help"
    )


@router.inline_query(F.query.startswith(","))
async def kaomoji_at_the_beginning(inline_query: InlineQuery, faces: list[str]):
    # When kaomoji is at the beginning, we still cut the text so not much info is sent,
    # so cut the original text if necessary, while removing the first comma
    if len(inline_query.query) <= max_chars:
        preview_text = inline_query.query[1:]
    else:
        preview_text = shorten(inline_query.query[1:])

    results = []
    for index, face in enumerate(faces):
        results.append(
            InlineQueryResultArticle(
                id=str(index),
                title=f"{face} {preview_text}",
                input_message_content=InputTextMessageContent(
                    message_text=f"{face} {inline_query.query[1:]}"
                )
            )
        )
    await inline_query.answer(
        results=results, cache_time=cache_time,
        switch_pm_text="Help and source code", switch_pm_parameter="help"
    )


@router.inline_query()
async def kaomoji_at_the_end(inline_query: InlineQuery, faces: list[str]):
    # We want to make sure that kaomoji is always visible,
    # so cut the original text if necessary
    if len(inline_query.query) <= max_chars:
        preview_text = inline_query.query
    else:
        preview_text = shorten(inline_query.query)

    results = []
    for index, face in enumerate(faces):
        results.append(
            InlineQueryResultArticle(
                id=str(index),
                title=f"{preview_text} {face}",
                input_message_content=InputTextMessageContent(
                    message_text=f"{inline_query.query} {face}"
                )
            )
        )
    await inline_query.answer(
        results=results, cache_time=cache_time,
        switch_pm_text="Help and source code", switch_pm_parameter="help"
    )
