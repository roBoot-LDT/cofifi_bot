from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database import save_feedback
from states import FEEDBACK_TEXT


async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите ваш комментарий или отзыв:")
    return FEEDBACK_TEXT


async def feedback_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_feedback(
        user_id=update.effective_user.id,
        username=update.effective_user.username or "",
        text=update.message.text,
    )
    await update.message.reply_text("Спасибо! Комментарий принят 🙌")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💬 Оставить комментарий$"), feedback_start)],
    states={
        FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_save)],
    },
    fallbacks=[],
)
