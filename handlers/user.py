from aiogram import Router, types, Bot
from aiogram.filters import CommandStart
from db.database import get_or_create_user
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def handle_start(msg: types.Message, state: FSMContext, bot: Bot):
    args = msg.text.split(maxsplit=1)
    args = args[1] if len(args) > 1 else None

    if args:
        await state.update_data(target_username=args)
        await msg.answer(f"پیامتو برای @{args} بنویس و بفرست 👇 (کاملاً ناشناس می‌مونی)")
    else:
        user = await get_or_create_user(msg.from_user)
        bot_info = await bot.get_me()
        link = f"https://t.me/{bot_info.username}?start={msg.from_user.username}"
        await msg.answer(
            f"""🔗 لینک ناشناس شما:
{link}"""
        )