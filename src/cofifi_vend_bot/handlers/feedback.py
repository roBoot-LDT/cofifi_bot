from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import FeedbackState
from database import save_feedback

router = Router()

@router.message(F.text == "💬 Оставить комментарий")
async def feedback_start(message: Message, state: FSMContext):
    await message.answer("Напишите ваш комментарий или отзыв:")
    await state.set_state(FeedbackState.text)

@router.message(FeedbackState.text)
async def feedback_save_handler(message: Message, state: FSMContext):
    await save_feedback(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        text=message.text,
    )
    await message.answer("Спасибо! Комментарий принят 🙌")
    await state.clear()
