from enum import Enum

class Language(Enum):
    en = "🇬🇧 English"
    pl = "🇵🇱 Polski"
    uk = "🇺🇦 Українська"
    ru = "🏳️‍🌈 Русский"

LANG_CODES = (lang.name for lang in Language)