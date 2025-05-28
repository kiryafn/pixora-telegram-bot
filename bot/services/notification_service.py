import html

from aiogram import Bot
from bot.models import User
from bot.models import JobListing
from bot.keyboards import get_link_keyboard
from bot.utils.i18n import _


class NotificationService:
    """
    Service responsible for sending job listing notifications to users via Telegram.

    Builds localized, HTML-formatted messages with job details and sends them
    as a photo message using Aiogram's Bot API.
    """

    async def notify_job_listing(self, bot: Bot, job: JobListing, user: User) -> None:
        """
        Sends a job listing notification to a specific user via Telegram.

        The message includes the job title, salary, location, company name, and
        company logo. All fields are localized based on the user's language setting
        and properly HTML-escaped.

        Args:
            bot (Bot): The Aiogram bot instance used to send the message.
            job (JobListing): The job listing to notify about.
            user (User): The user who will receive the message.
        """
        lines: list[str] = []

        # Add job title
        lines.append(f"<b>{html.escape(job.job_title)}</b>")
        lines.append("")

        # Localized field labels and values
        fields = {
            _("salary", lang=user.language): job.salary,
            _("location", lang=user.language): job.location,
            _("company", lang=user.language): job.company_name
        }

        for label, value in fields.items():
            lines.append(f"<b>{html.escape(label)}</b>: {html.escape(str(value))}")

        text = "\n".join(lines)

        # Send photo message with inline button
        await bot.send_photo(
            chat_id=user.id,
            caption=text,
            photo=job.company_logo_url,
            reply_markup=get_link_keyboard(lang=user.language, url=job.job_url)
        )


# Singleton instance for sending notifications
notification_service = NotificationService()