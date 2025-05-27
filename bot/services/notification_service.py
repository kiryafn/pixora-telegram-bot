from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.models import User
from bot.models.job_listing import JobListing
from bot.utils.i18n import _

class NotificationService:

    async def notify_job_listing(self, bot: Bot, job: JobListing, user: User):
        lines: list[str] = []

        lines.append(f"*{job.job_title}*")
        lines.append("")

        fields = {
            _("salary", lang=user.language):   job.salary,
            _("location", lang=user.language): job.location,
            _("company", lang=user.language):  job.company_name
        }

        for label, value in fields.items():
            lines.append(f"*{label}*: {value}")

        text = "\n".join(lines)

        kbbuilder = InlineKeyboardBuilder()
        kbbuilder.button(text=_("job_url", lang=user.language), url=job.job_url)


        await bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode="Markdown",
            reply_markup=kbbuilder.as_markup()
        )

notification_service = NotificationService()
