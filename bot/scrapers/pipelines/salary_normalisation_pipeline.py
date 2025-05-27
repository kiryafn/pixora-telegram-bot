import re

from bot.core import logger

class SalaryNormalizationPipeline:
    def process_item(self, item, spider):
        raw = item.get("salary")
        if not raw:
            item["salary"] = None
            return item

        parts = re.split(r"[–\-]", raw, maxsplit=1)
        lower = parts[0]

        cleaned = re.sub(r"[^\d,.]", "", lower)
        if not cleaned:
            item["salary"] = None
            return item

        try:
            num = float(cleaned.replace(",", "."))
            item["salary"] = int(num)
        except ValueError:
            logger.warning(f"Не удалось нормализовать зарплату: {raw!r}")
            item["salary"] = None

        return item