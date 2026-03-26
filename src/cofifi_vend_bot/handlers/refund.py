from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database import save_refund
from config import OWNER_CHAT_ID
from states import REFUND_POINT, REFUND_DATETIME, REFUND_AMOUNT, REFUND_REASON, REFUND_CONTACT
from keyboard import points_menu, contact_menu, main_menu


async def refund_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Укажите номер точки или автомата:", reply_markup=points_menu)
    return REFUND_POINT


async def refund_point(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["point"] = update.message.text
    await update.message.reply_text("Дата и примерное время покупки:")
    return REFUND_DATETIME


async def refund_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["datetime"] = update.message.text
    await update.message.reply_text("Сумма покупки:")
    return REFUND_AMOUNT


async def refund_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["amount"] = update.message.text
    await update.message.reply_text("Причина возврата:")
    return REFUND_REASON


async def refund_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reason"] = update.message.text
    await update.message.reply_text("Телефон или ник в Телеграме для связи (опционально):", reply_markup=contact_menu)
    return REFUND_CONTACT


async def refund_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    contact = update.message.text
    username = update.effective_user.username or ""

    save_refund(
        user_id=update.effective_user.id,
        username=username,
        point=data["point"],
        purchase_datetime=data["datetime"],
        amount=data["amount"],
        reason=data["reason"],
        contact=contact,
    )

    if OWNER_CHAT_ID:
        user_link = f"@{username}" if username else f"id{update.effective_user.id}"
        notify_text = (
            "🔔 <b>Новый запрос на возврат</b>\n\n"
            f"👤 Пользователь: {user_link}\n"
            f"📍 Точка: {data['point']}\n"
            f"🕐 Дата/время: {data['datetime']}\n"
            f"💰 Сумма: {data['amount']}\n"
            f"📝 Причина: {data['reason']}\n"
            f"📞 Контакт: {contact}"
        )
        await context.bot.send_message(OWNER_CHAT_ID, notify_text, parse_mode="HTML")

    await update.message.reply_text("Запрос принят. Мы рассмотрим его в ближайшее время. Спасибо!", reply_markup=main_menu)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💸 Запросить возврат$"), refund_start)],
    states={
        REFUND_POINT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, refund_point)],
        REFUND_DATETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, refund_datetime)],
        REFUND_AMOUNT:   [MessageHandler(filters.TEXT & ~filters.COMMAND, refund_amount)],
        REFUND_REASON:   [MessageHandler(filters.TEXT & ~filters.COMMAND, refund_reason)],
        REFUND_CONTACT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, refund_finish)],
    },
    fallbacks=[],
)
