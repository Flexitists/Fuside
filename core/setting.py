import json
import os
import tkinter as tk
from pathlib import Path
from typing import Any

try:
    import customtkinter as ctk
except ImportError:  # pragma: no cover - optional dependency in headless environments
    ctk = None

from tkinter import messagebox

_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "settings.json")
_DEFAULT_SETTINGS = {
    "theme_appearance": "System",
    "theme_color": "blue",
    "recent_files": [],
    "language": "en",
}
_LANGUAGE_CALLBACK = None
_THEME_CALLBACK = None


def set_settings_path(path: str) -> None:
    global _SETTINGS_PATH
    _SETTINGS_PATH = path


def _get_settings_path() -> str:
    return _SETTINGS_PATH


def _migrate_legacy_data(settings: dict[str, Any]) -> dict[str, Any]:
    root_dir = Path(__file__).resolve().parent.parent
    recent_json = root_dir / "assets" / "recent_files.json"
    theme_json = root_dir / "assets" / "theme.json"

    if recent_json.exists() and not settings.get("recent_files"):
        try:
            with recent_json.open("r", encoding="utf-8") as handle:
                legacy_data = json.load(handle)
            recent_files = legacy_data.get("recent_files", [])
            if isinstance(recent_files, list):
                settings["recent_files"] = recent_files
        except (json.JSONDecodeError, OSError):
            pass

    if theme_json.exists():
        try:
            with theme_json.open("r", encoding="utf-8") as handle:
                theme_data = json.load(handle)
            if isinstance(theme_data, dict):
                settings.setdefault("theme_appearance", theme_data.get("theme_appearance", "System"))
                settings.setdefault("theme_color", theme_data.get("theme_color", "blue"))
        except (json.JSONDecodeError, OSError):
            pass

    return settings


def _write_settings(data: dict[str, Any]) -> None:
    path = Path(_get_settings_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=4, ensure_ascii=False)


def _read_settings() -> dict[str, Any]:
    path = Path(_get_settings_path())
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def set_language_callback(callback) -> None:
    global _LANGUAGE_CALLBACK
    _LANGUAGE_CALLBACK = callback


def _notify_language_change(language: str) -> None:
    if _LANGUAGE_CALLBACK is not None:
        _LANGUAGE_CALLBACK(language)


def set_theme_callback(callback) -> None:
    global _THEME_CALLBACK
    _THEME_CALLBACK = callback


def _notify_theme_change(appearance_mode: str) -> None:
    if _THEME_CALLBACK is not None:
        _THEME_CALLBACK(appearance_mode)


def load_settings() -> dict[str, Any]:
    settings = dict(_DEFAULT_SETTINGS)
    settings.update(_read_settings())
    settings = _migrate_legacy_data(settings)
    settings.setdefault("theme_appearance", "System")
    settings.setdefault("theme_color", "blue")
    settings.setdefault("recent_files", [])
    settings.setdefault("language", "en")
    _write_settings(settings)
    return settings


def save_setting(values: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = load_settings()
    if values:
        settings.update(values)
    settings.setdefault("theme_appearance", "System")
    settings.setdefault("theme_color", "blue")
    settings.setdefault("recent_files", [])
    settings.setdefault("language", "en")
    _write_settings(settings)
    return settings


def get_setting(key: str, default: Any = None) -> Any:
    return load_settings().get(key, default)


def get_theme_settings() -> tuple[str, str]:
    settings = load_settings()
    return settings.get("theme_appearance", "System"), settings.get("theme_color", "blue")


def add_to_recent_files(file_path: str) -> None:
    settings = load_settings()
    recent_files = list(settings.get("recent_files", []))
    if file_path in recent_files:
        recent_files.remove(file_path)
    recent_files.insert(0, file_path)
    settings["recent_files"] = recent_files[:10]
    save_setting(settings)


def delete_from_recent_files(file_path: str) -> None:
    settings = load_settings()
    recent_files = list(settings.get("recent_files", []))
    if file_path in recent_files:
        recent_files.remove(file_path)
    settings["recent_files"] = recent_files
    save_setting(settings)


def delete_all_recent_files() -> None:
    settings = load_settings()
    settings["recent_files"] = []
    save_setting(settings)


def load_recent_files() -> list[str]:
    return list(load_settings().get("recent_files", []))


def open_settings(parent=None) -> None:
    if ctk is None:
        messagebox.showinfo("Settings", "customtkinter is not available.")
        return

    if parent is None:
        window = ctk.CTk()
    else:
        window = ctk.CTkToplevel(parent)

    window.title("Settings")
    window.resizable(False, False)
    icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
    if os.name == "nt":
        window.iconbitmap(icon_path)
    else:
        if os.path.exists(icon_path):
            icon_image = tk.PhotoImage(file=icon_path)
            window.iconphoto(False, icon_image)
            window._icon_image = icon_image

    current_appearance, current_color = get_theme_settings()
    current_language = str(get_setting("language", "en")).lower()
    appearance_var = tk.StringVar(value=current_appearance)
    color_var = tk.StringVar(value=current_color)
    language_var = tk.StringVar(value="English" if current_language == "en" else "Tiếng Việt")

    frame = ctk.CTkFrame(window)
    frame.pack(fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame, text="Appearance").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    appearance_box = ctk.CTkSegmentedButton(frame, values=["System", "Light", "Dark"], variable=appearance_var)
    appearance_box.grid(row=0, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame, text="Color").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    color_box = ctk.CTkSegmentedButton(frame, values=["blue", "green", "dark-blue"], variable=color_var)
    color_box.grid(row=1, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame, text="Language").grid(row=2, column=0, padx=10, pady=8, sticky="w")
    language_box = ctk.CTkSegmentedButton(frame, values=["English", "Tiếng Việt"], variable=language_var)
    language_box.grid(row=2, column=1, padx=10, pady=8)

    def apply_settings() -> None:
        selected_language = "en" if language_var.get() == "English" else "vi"
        settings = save_setting({
            "theme_appearance": appearance_var.get(),
            "theme_color": color_var.get(),
            "language": selected_language,
        })
        ctk.set_appearance_mode(settings["theme_appearance"])
        ctk.set_default_color_theme(settings["theme_color"])
        _notify_theme_change(settings["theme_appearance"])
        _notify_language_change(selected_language)
        messagebox.showinfo("Applied", "Restart Fuside to change the interface!")

    ctk.CTkButton(frame, text="Apply", command=apply_settings).grid(row=3, column=1, padx=10, pady=12, sticky="e")

    if parent is None:
        window.mainloop()
