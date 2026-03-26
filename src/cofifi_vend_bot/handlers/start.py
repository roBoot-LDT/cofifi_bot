from telegram import Update
from telegram.ext import ContextTypes
from keyboard import main_menu


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помощник сервиса кофе-корнеров.\nЧем могу помочь?",
        reply_markup=main_menu
    )
