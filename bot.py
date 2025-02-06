import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from datetime import datetime, timedelta
from config import TOKEN_v2, GROUP_ID


bot = Bot(token=TOKEN_v2)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

USER_ACTIVITY = {}

async def check_user_activity():
    while True:
        current_time = datetime.now()
        for user_id, last_message_time in list(USER_ACTIVITY.items()):
            if current_time - last_message_time > timedelta(hours=24):
                try:
                    await bot.kick_chat_member(chat_id=GROUP_ID, user_id=user_id)
                    del USER_ACTIVITY[user_id]
                    print(f"User {user_id} kicked for inactivity")
                except Exception as e:
                    print(f"Error kicking user {user_id}: {e}")
        await asyncio.sleep(1)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    USER_ACTIVITY[message.from_user.id] = datetime.now()
    await message.reply("Salom! Bu bot orqali sizni kuzatib boraman!")



@dp.message_handler()
async def track_activity(message: types.Message):
    USER_ACTIVITY[message.from_user.id] = datetime.now()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_user_activity())

    executor.start_polling(dp, skip_updates=True)
