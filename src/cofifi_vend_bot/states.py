from aiogram.fsm.state import StatesGroup, State

class FeedbackState(StatesGroup):
    text = State()

class RefundState(StatesGroup):
    point = State()
    datetime = State()
    amount = State()
    reason = State()
    contact = State()
