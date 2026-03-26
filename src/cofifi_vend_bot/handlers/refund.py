from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import RefundState
from database import save_refund
from config import OWNER_CHAT_ID

router = Router()


@router.message(F.text == "💸 Запросить возврат")
async def refund_start(message: Message, state: FSMContext):
    await message.answer("Укажите номер точки или автомата:")
    await state.set_state(RefundState.point)


@router.message(RefundState.point)
async def refund_point(message: Message, state: FSMContext):
    await state.update_data(point=message.text)
    await message.answer("Дата и примерное время покупки:")
    await state.set_state(RefundState.datetime)


@router.message(RefundState.datetime)
async def refund_datetime(message: Message, state: FSMContext):
    await state.update_data(datetime=message.text)
    await message.answer("Сумма покупки:")
    await state.set_state(RefundState.amount)


@router.message(RefundState.amount)
async def refund_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.answer("Причина возврата:")
    await state.set_state(RefundState.reason)


@router.message(RefundState.reason)
async def refund_reason(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("Телефон или ник в Телеграме для связи:")
    await state.set_state(RefundState.contact)


@router.message(RefundState.contact)
async def refund_finish(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    contact = message.text
    username = message.from_user.username or ""

    await save_refund(
        user_id=message.from_user.id,
        username=username,
        point=data["point"],
        purchase_datetime=data["datetime"],
        amount=data["amount"],
        reason=data["reason"],
        contact=contact,
    )

    if OWNER_CHAT_ID:
        user_link = f"@{username}" if username else f"id{message.from_user.id}"
        notify_text = (
            "🔔 <b>Новый запрос на возврат</b>\n\n"
            f"👤 Пользователь: {user_link}\n"
            f"📍 Точка: {data['point']}\n"
            f"🕐 Дата/время: {data['datetime']}\n"
            f"💰 Сумма: {data['amount']}\n"
            f"📝 Причина: {data['reason']}\n"
            f"📞 Контакт: {contact}"
        )
        await bot.send_message(OWNER_CHAT_ID, notify_text, parse_mode="HTML")

    await message.answer("Запрос принят. Мы рассмотрим его в ближайшее время.")
    await state.clear()
