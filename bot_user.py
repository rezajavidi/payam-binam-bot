
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_queue_manager import add_user_to_queue
from bot_connector import try_connect_user, active_chats

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

@router.message(F.text.regexp(r'^/start\s+\d+'))
async def deep_link_connect(msg: Message):
    parts = msg.text.split()
    target_id = int(parts[1])
    visitor_id = msg.from_user.id
    # ثبت اتصال مستقیم
    active_chats[visitor_id] = target_id
    active_chats[target_id] = visitor_id
    await msg.answer("✅ اتصال برقرار شد! می‌توانید پیام بفرستید.")
    await msg.bot.send_message(target_id, "✅ شما با یک کاربر ناشناس متصل شدید، گفتگو کنید!")

@router.message(F.text == "/start")
async def start(msg: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 دریافت پیام ناشناس با لینک", callback_data="mode_link")],
        [InlineKeyboardButton(text="💬 چت ناشناس دو نفره", callback_data="mode_chat")]
    ])
    await msg.answer("سلام! می‌خوای چی‌کار کنی؟", reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == "mode_chat")
async def choose_chat_mode(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text("برای شروع چت ناشناس، ابتدا جنسیتت رو انتخاب کن:",
                               reply_markup=kb(GENDERS))
    await state.set_state(ProfileStates.gender)
    await cb.answer()

@router.callback_query(F.data == "mode_link")
async def choose_link_mode(cb: CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    me = await cb.bot.get_me()
    username = me.username
    link = f"https://t.me/{username}?start={user_id}"
    await cb.message.edit_text(
        f"""✅ لینک دریافت پیام ناشناس تو:

{link}

این لینک رو برای دوستات بفرست تا بتونن ناشناس برات پیام بفرستن!"""
    )
    await cb.answer()

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
