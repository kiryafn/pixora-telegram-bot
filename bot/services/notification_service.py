from aiogram import Bot
from bot.models import User
from bot.models import JobListing
from bot.keyboards import get_link_keyboard
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


        await bot.send_photo(
            chat_id=user.id,
            caption=text,
            photo=job.company_logo_url,
            parse_mode="Markdown",
            reply_markup=get_link_keyboard(lang=user.language, url=job.job_url)
        )

notification_service = NotificationService()
