from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Оставить комментарий")],
        [KeyboardButton(text="💸 Запросить возврат")]
    ],
    resize_keyboard=True
)
