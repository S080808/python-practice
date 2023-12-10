import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import handlers
from config import API_TOKEN
from data.database import DataBase

bot = Bot(API_TOKEN, parse_mode="HTML")
dp = Dispatcher()
db = DataBase()

async def setup_bot_commands():
    """
    Creates "keyboard" menu which helps user to navigate the bot
    """
    bot_commands = [
        BotCommand(command="/start", description="Запустить бота."),
        BotCommand(command="/myprofile", description="Обновить данные профиля."),
        BotCommand(command="/editprofile", description="Заполнить анкету знакомств."),
        BotCommand(command="/help", description="Вопросы по интерфейсу бота.")
    ]
    await bot.set_my_commands(bot_commands)

async def main():
    with open("data/users.db", "w") as f:
        f.write("")
    await db.create_table()
    await setup_bot_commands()
    dp.include_routers(
        handlers.callbacks.router,
        handlers.commands.router,
        handlers.sign_up.router,
        handlers.menu.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())