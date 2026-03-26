from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import FeedbackState
from aiogram import F

router = Router()

@router.message(F.text == "💬 Оставить комментарий")
async def feedback_start(message: Message, state: FSMContext):
    await message.answer("Напишите ваш комментарий или отзыв:")
    await state.set_state(FeedbackState.text)

@router.message(FeedbackState.text)
async def feedback_save(message: Message, state: FSMContext):
    text = message.text

    # TODO: сохранить в БД / Google Sheets
    print(f"Комментарий от {message.from_user.id}: {text}")

    await message.answer("Спасибо! Комментарий принят 🙌")
    await state.clear()
