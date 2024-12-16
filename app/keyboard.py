from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Spoiler


def note_message(
    id_: int | str,
    name: str,
    description: str,
    *,
    more: int | None = None,
    example: int | None = None,
):
    content = Text(name, "\n", Spoiler(description))
    inline_btn_1 = InlineKeyboardButton(text="👍", callback_data=f'note:useful:{id_}')
    inline_btn_2 = InlineKeyboardButton(text="👎", callback_data=f'note:not_useful:{id_}')
    inline_btn_3 = InlineKeyboardButton(text="💬", callback_data=f'note:comment:{id_}')
    rows=[[inline_btn_1, inline_btn_2, inline_btn_3]]
    if more:
        rows.append([InlineKeyboardButton(text="Подробнее", callback_data=f'more:{more}')])
    if example:
        rows.append([InlineKeyboardButton(text="Примеры", callback_data=f'example:{example}')])
    return {
        **content.as_kwargs(),
        "reply_markup": InlineKeyboardMarkup(inline_keyboard=rows)
    }
