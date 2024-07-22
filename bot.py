import logging
import asyncio
from aiogram.types import BotCommand
from bot_instance import bot, dp
from handlers import *
from scheduler import setup_scheduler
from currency import update_currency_rates


async def on_startup(dp):
    await update_currency_rates()
    setup_scheduler()

    # Настроить команды бота
    commands = [
        BotCommand(command="/rates", description="Get the current exchange rates for all currencies"),
        BotCommand(command="/exchange", description="Convert an amount from one currency to another, <currency_from> "
                                                    "<currency_to> <amount> - convert the amount from "
                                                    "one currency to another"),
        BotCommand(command="/help", description="Show help message")
    ]
    await bot.set_my_commands(commands)


async def main():
    await on_startup(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
