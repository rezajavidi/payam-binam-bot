from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_connector import try_connect_user
from database import add_user_to_db

router = Router()

class StartStates(StatesGroup):
    choice = State()
    link_emoji = State()

class ProfileStates(StatesGroup):
    gender = State()
    age = State()
    city = State()
    target_gender = State()
    target_city = State()
    emoji = State()

GENDERS = [("male", "👨 پسر"), ("female", "👩 دختر")]
CITIES = ["تهران", "اصفهان", "تبریز", "مشهد", "شیراز", "رشت", "بندرعباس"]

def kb(items):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=value)] for value, label in items
    ])

@router.message(F.command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    args = msg.get_args()
    await state.clear()
    if args:
        # Deep link payload: direct anonymous message to specific user
        await msg.answer("برای شروع چت ناشناس، لطفا یک ایموجی برای نمایش خود انتخاب کن:")
        await state.update_data(link_target=int(args))
        await state.set_state(StartStates.link_emoji)
    else:
        items = [("link", "📨 دریافت لینک ناشناس شخصی"), ("connect", "🔗 متصل شدن به یک ناشناس")]
        await msg.answer("لطفا یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=kb(items))
        await state.set_state(StartStates.choice)

@router.callback_query(StartStates.choice)
async def start_choice(cb: CallbackQuery, state: FSMContext):
    choice = cb.data
    if choice == "connect":
        await cb.message.edit_text("سلام! برای شروع چت ناشناس، ابتدا جنسیتت رو انتخاب کن:", reply_markup=kb(GENDERS))
        await state.set_state(ProfileStates.gender)
    elif choice == "link":
        me = await cb.message.bot.get_me()
        link = f"https://t.me/{me.username}?start={cb.from_user.id}"
        await cb.message.edit_text(f"لینک ناشناس شخصی شما:\n{link}")
        await state.clear()
    await cb.answer()

@router.message(StartStates.link_emoji)
async def deep_link_emoji(msg: Message, state: FSMContext):
    emoji = msg.text.strip()
    data = await state.get_data()
    target = data.get("link_target")
    # Directly connect sender and target with emoji
    await try_connect_user(msg, {"emoji": emoji, "direct_target": target})
    await state.clear()

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
    await cb.message.edit_text("جنسیت مخاطب رو انتخاب کن:", reply_markup=kb(GENDERS + [("any", "هرکدام")]))
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
async def choose_target_city(cb: CallbackQuery, state: FSMContext):
    await state.update_data(target_city=cb.data)
    await cb.message.edit_text("لطفا یک ایموجی برای نمایش خود انتخاب کن:")
    await state.set_state(ProfileStates.emoji)
    await cb.answer()

@router.message(ProfileStates.emoji)
async def choose_emoji(msg: Message, state: FSMContext):
    emoji = msg.text.strip()
    await state.update_data(emoji=emoji)
    data = await state.get_data()
    # ذخیره پروفایل کاربر در پایگاه داده
    add_user_to_db(
        user_id=msg.from_user.id,
        first_name=msg.from_user.first_name or "",
        username=msg.from_user.username or "",
        age=data.get("age"),
        gender=data.get("gender"),
        city=data.get("city")
    )
    await state.clear()
    await try_connect_user(msg, data)
