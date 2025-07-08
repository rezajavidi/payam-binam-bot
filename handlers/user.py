from aiogram import Router, types
from aiogram.filters import CommandStart
from db.database import get_or_create_user
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def handle_start(msg: types.Message, state: FSMContext):
    args = msg.get_args()
    if args:
        await state.update_data(target_username=args)
        await msg.answer(f"پیامتو برای @{args} بنویس و بفرست 👇 (کاملاً ناشناس می‌مونی)")
    else:
        user = await get_or_create_user(msg.from_user)
        await msg.answer(f"🔗 لینک ناشناس شما:
https://t.me/YOUR_BOT_USERNAME?start={msg.from_user.username}")