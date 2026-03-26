from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database import save_feedback
from states import FEEDBACK_TEXT
from config import OWNER_CHAT_ID
from keyboard import main_menu


async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите ваш комментарий или отзыв:")
    return FEEDBACK_TEXT


async def feedback_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_feedback(
        user_id=update.effective_user.id,
        username=update.effective_user.username or "",
        text=update.message.text,
    )
    await update.message.reply_text("Спасибо! Комментарий принят 🙌", reply_markup=main_menu)
    if OWNER_CHAT_ID:
        username = update.effective_user.username or ""
        user_link = f"@{username}" if username else f"id{update.effective_user.id}"
        notify_text = (
            "💬 <b>Новый комментарий</b>\n\n"
            f"👤 Пользователь: {user_link}\n"
            f"📝 Текст: {update.message.text}"
        )
        await context.bot.send_message(OWNER_CHAT_ID, notify_text, parse_mode="HTML")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💬 Оставить комментарий$"), feedback_start)],
    states={
        FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_save)],
    },
    fallbacks=[],
)
