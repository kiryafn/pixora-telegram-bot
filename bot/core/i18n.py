import json
from pathlib import Path
from typing import Dict

class Translator:
    def __init__(self, default_locale: str = "en"):
        self.default_locale: str = default_locale
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()

    def load_translations(self):
        locales_path: Path = Path(__file__).parent.parent.parent / "locales"
        for locale_file in locales_path.glob("*.json"):
            lang: str = locale_file.stem
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Failed to load {locale_file}")

    def gettext(self, key: str, lang: str) -> str:
        return (
            self.translations.get(lang, {}).get(key)
            or self.translations.get(self.default_locale, {}).get(key)
            or key
        )

translator: Translator = Translator()

def _(key: str, lang: str) -> str:
    return translator.gettext(key, lang)