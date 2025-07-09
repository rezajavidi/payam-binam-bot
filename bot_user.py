from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_connector import direct_connect_user

router = Router()

class LinkStates(StatesGroup):
    emoji = State()

@router.message(F.command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    args = msg.get_args()
    await state.clear()
    if args:
        # Deep link click: Person2 flow
        # args is target user_id
        await msg.answer("برای شروع چت ناشناس، لطفا یک ایموجی برای نمایش خود انتخاب کن:")
        await state.update_data(link_target=int(args))
        await state.set_state(LinkStates.emoji)
    else:
        # Person1 flow: generate personal link
        me = await msg.bot.get_me()
        link = f"https://t.me/{me.username}?start={msg.from_user.id}"
        await msg.answer(f"لینک ناشناس شخصی شما:\n{link}")

@router.message(LinkStates.emoji)
async def choose_emoji(msg: Message, state: FSMContext):
    data = await state.get_data()
    target = data.get("link_target")
    emoji = msg.text.strip()
    await state.clear()
    # Connect Person2 (msg.from_user) with Person1 (target)
    await direct_connect_user(msg, emoji, target)