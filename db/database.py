from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from db.models import Base, User, Message

DATABASE_URL = "sqlite+aiosqlite:///payambinam.db"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_or_create_user(tg_user):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_user.id))
        user = result.scalars().first()
        if not user:
            user = User(tg_id=tg_user.id, username=tg_user.username, name=tg_user.full_name)
            session.add(user)
            await session.commit()
        return user

async def get_user_by_username(username):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalars().first()

async def save_message(receiver_id, text):
    async with SessionLocal() as session:
        msg = Message(receiver_id=receiver_id, text=text)
        session.add(msg)
        await session.commit()