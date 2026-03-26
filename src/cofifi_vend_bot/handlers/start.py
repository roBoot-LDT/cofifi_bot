from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboard import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я помощник сервиса кофе-корнеров.\n"
        "Чем могу помочь?",
        reply_markup=main_menu
    )
