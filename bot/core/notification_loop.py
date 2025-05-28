import asyncio
from aiogram import Bot

from bot.core import logger
from bot.services import (
    user_service,
    job_preference_service,
    listing_preference_service,
    notification_service,
    job_listing_service,
)

async def _process_user(bot: Bot, user):
    pref = await job_preference_service.get_preference_by_user_id(user.id)
    if not pref:
        logger.warning(f"User {user.id} has no preferences, skip")
        return

    unseen = await listing_preference_service.get_all_unseen_by_preference_id(pref.id)
    for lp in unseen:
        vacancy = await job_listing_service.get_by_id(lp.job_listing_id)
        if not vacancy:
            continue

        await notification_service.notify_job_listing(bot, vacancy, user)

        lp.is_seen = True
        await listing_preference_service.save(lp)

        await asyncio.sleep(3)

async def notify_users_about_new_jobs(bot: Bot) -> None:
    users = await user_service.get_all_active()
    tasks = [asyncio.create_task(_process_user(bot, user)) for user in users]
    if tasks:
        await asyncio.gather(*tasks)

async def main_notify_loop(bot: Bot) -> None:
    while True:
        try:
            await notify_users_about_new_jobs(bot)
        except Exception as e:
            logger.error(f"Error in notification loop: {e!r}")
        await asyncio.sleep(60*60)