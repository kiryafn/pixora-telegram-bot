from aiogram import Dispatcher
from bot.handlers import routers

def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    return dp