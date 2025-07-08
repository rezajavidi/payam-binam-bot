from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from db.database import get_user_by_username, save_message

router = Router()

@router.message()
async def receive_anonymous_message(msg: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if "target_username" in data:
        target = await get_user_by_username(data["target_username"])
        if target:
            await bot.send_message(
                target.tg_id,
                f"""📩 پیام بی‌نام برات اومده:

{msg.text}"""
            )
            await save_message(target.id, msg.text)
            await msg.answer("✅ پیام ناشناس ارسال شد.")
        else:
            await msg.answer("❌ کاربر مورد نظر پیدا نشد.")
        await state.clear()