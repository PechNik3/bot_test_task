import logging  # Добавьте эту строку
from aiogram.filters import Command
from aiogram import types
from bot_instance import dp
from redis_utils import init_redis

r = init_redis()


@dp.message(Command('rates'))
async def send_rates(message: types.Message):
    logging.info("Fetching currency rates...")
    try:
        rates = {}
        for key in r.keys('*'):
            value = r.get(key).decode('utf-8')
            rates[key.decode('utf-8')] = value

        if rates:
            rates_message = "\n".join([f"{key}: {value}" for key, value in rates.items()])
            # Разбиваем сообщение на части, если оно слишком длинное
            MAX_MESSAGE_LENGTH = 4096
            for i in range(0, len(rates_message), MAX_MESSAGE_LENGTH):
                await message.answer(rates_message[i:i + MAX_MESSAGE_LENGTH])
        else:
            await message.answer("No currency rates available.(Курс валют не доступен.)")
    except Exception as e:
        logging.error(f"Error fetching rates: {e}")
        await message.answer("Error fetching rates.(Ошибка при получении курсов валют.)")


@dp.message(Command('exchange'))
async def send_exchange(message: types.Message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            await message.answer("Format: /exchange <from_currency> <to_currency> <amount>\n"
                                 "(Формат команды: /exchange <валюта_от> <валюта_до> <сумма>)")
            return

        from_currency, to_currency, amount = parts[1].upper(), parts[2].upper(), float(parts[3])

        from_rate, to_rate = r.get(from_currency), r.get(to_currency)

        if from_rate is None or to_rate is None:
            await message.answer("Error: One of the specified currencies is not available."
                                 "(Ошибка: одна из указанных валют недоступна.)")
            return

        result = (amount * float(from_rate.decode('utf-8'))) / float(to_rate.decode('utf-8'))
        await message.answer(f"{amount} {from_currency} = {result:.2f} {to_currency}")

    except ValueError:
        await message.answer("Error: Invalid amount or currency code.(Ошибка: неверная сумма или код валюты.)")
    except Exception as e:
        logging.error(f"Error processing exchange: {e}")
        await message.answer(
            "Error processing your request. Make sure you use the format: "
            "/exchange <from_currency> <to_currency> <amount>(Ошибка при обработке запроса. Убедитесь, что используете"
            " формат: /exchange <валюта_от> <валюта_до> <сумма>)")


@dp.message(Command('help'))
async def send_help(message: types.Message):
    help_text = (
        "Here are the available commands(Доступные команды):\n"
        "/rates - Get the current exchange rates for all available currencies"
        "(Получить текущие курсы всех доступных валют)\n"
        "/exchange <from_currency> <to_currency> <amount> - Convert an amount from one currency to another"
        "(<валюта_от> <валюта_до> <сумма> - Конвертировать сумму из одной валюты в другую)\n"
        "/help - Show list of commands(Показать список команд)"
    )
    await message.answer(help_text)
