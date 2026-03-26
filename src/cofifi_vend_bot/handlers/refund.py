from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import RefundState
from aiogram import F

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
    await state.set_state(RefundState.contact)

@router.message(RefundState.contact)
async def refund_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Телефон или ник-нейм в телеграмме:")
    await state.set_state(RefundState.reason)

@router.message(RefundState.reason)
async def refund_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    data["reason"] = message.text

    # TODO: сохранить + уведомить оператора
    print(f"Возврат: {data}")

    await message.answer(
        "Запрос принят. Мы рассмотрим его в ближайшее время."
    )
    await state.clear()
