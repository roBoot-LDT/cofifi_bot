from telegram import ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    [
        ["💬 Оставить комментарий"],
        ["💸 Запросить возврат"]
    ],
    resize_keyboard=True
)
