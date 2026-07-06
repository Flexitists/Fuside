import json
import os
from pathlib import Path
from typing import Any

from core import setting

_TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translation"


def _load_translation_data() -> dict[str, dict[str, str]]:
    translations: dict[str, dict[str, str]] = {}
    for translation_file in _TRANSLATIONS_DIR.glob("*.json"):
        try:
            with translation_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                translations[translation_file.stem] = data
        except (OSError, json.JSONDecodeError):
            continue
    return translations


_TRANSLATIONS = _load_translation_data()


def set_language(language: str) -> str:
    language = language.lower()
    if language in {"vi", "vn"}:
        language = "vi"
    elif language not in _TRANSLATIONS and language != "en":
        language = "en"
    setting.save_setting({"language": language})
    return language


def get_language() -> str:
    language = str(setting.get_setting("language", "en")).lower()
    if language in {"vi", "vn"}:
        return "vi"
    return language


def t(key: str, default: str | None = None) -> str:
    language = get_language()
    if language == "en":
        translations = _TRANSLATIONS.get("en", {})
    else:
        translations = _TRANSLATIONS.get("vn", {}) if language == "vi" else _TRANSLATIONS.get(language, {})

    if key in translations:
        return translations[key]
    if default is not None:
        return default
    return key
