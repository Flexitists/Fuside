import json
import os
import customtkinter as ctk
from tkinter import messagebox


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
THEME_PATH = os.path.join(BASE_DIR, "assents", "theme.json")
ICON_PATH = os.path.join(BASE_DIR,  "assents", "icon.ico")

DEFAULT_THEME = {
    "theme_appearance": "Dark",
    "theme_color": "blue",
}


def load_theme_config():
    """Load theme configuration from disk, falling back to defaults."""
    data = DEFAULT_THEME.copy()
    try:
        with open(THEME_PATH, "r", encoding="utf-8") as theme_file:
            loaded = json.load(theme_file)
            if isinstance(loaded, dict):
                data.update(loaded)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return data


def save_theme_config(data):
    """Persist theme configuration to disk."""
    with open(THEME_PATH, "w", encoding="utf-8") as theme_file:
        json.dump(data, theme_file, indent=2)


class SettingWindow(ctk.CTkToplevel):
    """Settings window for Fuside."""

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Fuside Settings")
        self.geometry("795x565")
        #// self.minsize(620, 400)
        self.resizable(False, False)

        #//try:
        self.iconbitmap(ICON_PATH)
        #//except Exception:
        #//    pass

        self.theme_data = load_theme_config()

        self._build_ui()
        self._load_values()

        self.transient(master)
        self.grab_set()

    def _build_ui(self):
        outer = ctk.CTkFrame(self, corner_radius=16)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", padx=6, pady=(6, 12))

        ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text="Personalize Fuside's look and save it to theme.json.",
            text_color=("gray35", "gray75"),
        ).pack(anchor="w", pady=(4, 0))

        body = ctk.CTkFrame(outer, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=6)

        left = ctk.CTkFrame(body, width=200, corner_radius=14)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="Categories",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))

        self.category_list = ctk.CTkSegmentedButton(
            left,
            values=["Appearance", "About"],
            command=self._show_page,
        )
        self.category_list.set("Appearance")
        self.category_list.pack(fill="x", padx=14, pady=(0, 14))

        self.right = ctk.CTkFrame(body, corner_radius=14)
        self.right.pack(side="left", fill="both", expand=True)

        self.appearance_page = ctk.CTkFrame(self.right, fg_color="transparent")
        self.about_page = ctk.CTkFrame(self.right, fg_color="transparent")

        self._build_appearance_page()
        self._build_about_page()
        self._show_page("Appearance")

        button_bar = ctk.CTkFrame(outer, fg_color="transparent")
        button_bar.pack(fill="x", padx=6, pady=(10, 4))

        ctk.CTkButton(
            button_bar,
            text="Reset to Defaults",
            fg_color="gray30",
            hover_color="gray40",
            command=self.reset_defaults,
            width=140,
        ).pack(side="left")

        ctk.CTkButton(
            button_bar,
            text="Save Changes",
            command=self.save_changes,
            width=140,
        ).pack(side="right")

    def _build_appearance_page(self):
        page = self.appearance_page
        page.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            page,
            text="Appearance",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            page,
            text="Choose the application appearance and color theme.",
            text_color=("gray35", "gray75"),
        ).pack(anchor="w", pady=(4, 18))

        form = ctk.CTkFrame(page, fg_color="transparent")
        form.pack(fill="x")

        ctk.CTkLabel(form, text="Theme mode").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.appearance_var = ctk.StringVar()
        self.appearance_option = ctk.CTkSegmentedButton(
            form,
            values=["System", "Light", "Dark"],
            variable=self.appearance_var,
        )
        self.appearance_option.grid(row=0, column=1, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(form, text="Accent color").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.color_var = ctk.StringVar()
        self.color_option = ctk.CTkSegmentedButton(
            form,
            values=["blue", "green", "dark-blue"],
            variable=self.color_var,
        )
        self.color_option.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        form.grid_columnconfigure(1, weight=1)

        note = ctk.CTkFrame(page, fg_color=("gray92", "gray18"), corner_radius=12)
        note.pack(fill="x", pady=(12, 0))
        ctk.CTkLabel(
            note,
            text=(
                "Tip: appearance changes apply immediately. "
                "Color theme is saved for the next launch too."
            ),
            justify="left",
            wraplength=300,
            text_color=("gray25", "gray80"),
        ).pack(anchor="w", padx=14, pady=12)

    def _build_about_page(self):
        page = self.about_page

        ctk.CTkLabel(
            page,
            text="About Fuside",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=18, pady=(18, 6))

        about_box = ctk.CTkFrame(page, corner_radius=12)
        about_box.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        lines = [
            "Fuside is a lightweight Python IDE built with CustomTkinter.",
            "Theme values are read from assents/theme.json on startup.",
            "You can safely extend this panel with editor preferences later.",
        ]
        for line in lines:
            ctk.CTkLabel(
                about_box,
                text=line,
                anchor="w",
                justify="left",
                wraplength=320,
            ).pack(anchor="w", padx=14, pady=(12, 0))

    def _show_page(self, page_name):
        """Switch the visible settings category."""
        self.appearance_page.pack_forget()
        self.about_page.pack_forget()

        if page_name == "About":
            self.about_page.pack(fill="both", expand=True, padx=18, pady=18)
        else:
            self.appearance_page.pack(fill="both", expand=True, padx=18, pady=18)

    def _load_values(self):
        self.appearance_var.set(self.theme_data.get("theme_appearance", "Dark"))
        self.color_var.set(self.theme_data.get("theme_color", "blue"))

    def reset_defaults(self):
        self.appearance_var.set(DEFAULT_THEME["theme_appearance"])
        self.color_var.set(DEFAULT_THEME["theme_color"])

    def save_changes(self):
        self.theme_data["theme_appearance"] = self.appearance_var.get()
        self.theme_data["theme_color"] = self.color_var.get()
        save_theme_config(self.theme_data)

        messagebox.showinfo(
            "Settings Saved",
            "Restart Fuside to apply!",
        )


def open_settings(master=None):
    """Open the settings window."""
    return SettingWindow(master)
