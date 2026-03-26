from telegram import ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    [
        ["💬 Оставить комментарий"],
        ["💸 Запросить возврат"]
    ],
    resize_keyboard=True
)

points_menu = ReplyKeyboardMarkup(
    [
        ["О`Компы"],
        ["ТЦ Можайское шоссе 121"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

contact_menu = ReplyKeyboardMarkup(
    [
        ["Не оставлять контактные данные"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
