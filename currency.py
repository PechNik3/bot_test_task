import aiohttp
import xml.etree.ElementTree as ET
import logging
from redis_utils import init_redis

r = init_redis()


async def fetch_currency_rates():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    root = ET.fromstring(data)

                    rates_updated = False
                    for currency in root.findall('Valute'):
                        char_code = currency.find('CharCode').text
                        value = currency.find('Value').text.replace(',', '.')
                        r.set(char_code, value)
                        logging.info(f"Saved {char_code} to Redis with value {value}")
                        rates_updated = True

                    # Убедитесь, что RUB установлен
                    if not r.get('RUB'):
                        r.set('RUB', '1.0')  # Установите значение по умолчанию
                        logging.info("RUB not found in Redis, setting default value to 1.0")

                    if rates_updated:
                        logging.info("Currency rates updated in Redis.")
                    else:
                        logging.warning("No currency rates were updated.")
                else:
                    logging.error(f"Failed to fetch currency rates: {response.status}")
    except aiohttp.ClientError as e:
        logging.error(f"Failed to fetch currency rates due to network error: {e}")
    except ET.ParseError as e:
        logging.error(f"Failed to parse XML data: {e}")


async def update_currency_rates():
    await fetch_currency_rates()
