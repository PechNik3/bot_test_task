from apscheduler.schedulers.asyncio import AsyncIOScheduler
from currency import update_currency_rates

scheduler = AsyncIOScheduler()


def setup_scheduler():
    # Настроить ежедневное обновление курсов валют
    scheduler.add_job(update_currency_rates, 'interval', days=1)
    scheduler.start()
