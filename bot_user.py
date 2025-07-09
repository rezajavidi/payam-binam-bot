from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_queue_manager import add_user_to_queue
from bot_connector import try_connect_user

router = Router()

class ProfileStates(StatesGroup):
    gender = State()
    age = State()
    city = State()
    target_gender = State()
    target_city = State()

GENDERS = [("male", "👨 پسر"), ("female", "👩 دختر")]
CITIES = ["تهران", "اصفهان", "تبریز", "مشهد", "شیراز", "رشت", "بندرعباس"]

def kb(items):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=value)] for value, label in items
    ])

@router.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    await msg.answer(
        "سلام! برای شروع چت ناشناس، ابتدا جنسیتت رو انتخاب کن:",
        reply_markup=kb(GENDERS)
    )
    await state.set_state(ProfileStates.gender)

@router.callback_query(ProfileStates.gender)
async def choose_gender(cb: CallbackQuery, state: FSMContext):
    await state.update_data(gender=cb.data)
    await cb.message.edit_text("سن خودت رو وارد کن (مثلاً 23):")
    await state.set_state(ProfileStates.age)
    await cb.answer()

@router.message(ProfileStates.age, F.text.isdigit())
async def choose_age(msg: Message, state: FSMContext):
    await state.update_data(age=int(msg.text))
    items = [(c, c) for c in CITIES]
    await msg.answer("شهر خودت رو انتخاب کن:", reply_markup=kb(items))
    await state.set_state(ProfileStates.city)

@router.callback_query(ProfileStates.city)
async def choose_city(cb: CallbackQuery, state: FSMContext):
    await state.update_data(city=cb.data)
    await cb.message.edit_text("جنسیت مخاطب رو انتخاب کن:", reply_markup=kb(GENDERS+[("any","هرکدام")]))
    await state.set_state(ProfileStates.target_gender)
    await cb.answer()

@router.callback_query(ProfileStates.target_gender)
async def choose_target_gender(cb: CallbackQuery, state: FSMContext):
    await state.update_data(target_gender=cb.data)
    items = [(c, c) for c in CITIES] + [("any", "فرقی نمی‌کند")]
    await cb.message.edit_text("شهر مخاطب رو انتخاب کن:", reply_markup=kb(items))
    await state.set_state(ProfileStates.target_city)
    await cb.answer()

@router.callback_query(ProfileStates.target_city)
async def finish_profile(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["target_city"] = cb.data
    await state.clear()

    # اضافه به صف و تلاش برای اتصال
    await try_connect_user(cb.message, data)
    await cb.answer()