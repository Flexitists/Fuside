import customtkinter as ctk
import os
import tkinter as tk
from CTkMenuBar import *

from gui.terminal import Terminal
from gui.editor import Editor
from gui.recent_bar import Sidebar
from core import menu_command, file_manager, setting, i18n

# Load theme configuration from shared settings
appearance, color = setting.get_theme_settings()
ctk.set_appearance_mode(appearance)
ctk.set_default_color_theme(color)


root = ctk.CTk()
root.title("Fuside")
if os.name == "nt":
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "assets", "icon.ico"))
else:
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
    if os.path.exists(icon_path):
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(False, icon_image)
        root._icon_image = icon_image
root.geometry("1000x625")

# Menu - pass theme data to ensure synchronization
menus = CTkMenuBar(root)
# File
file_btn = menus.add_cascade(i18n.t("file"))
file_menu = CustomDropdownMenu(widget=file_btn)

file_menu.add_option(
            option=i18n.t("new_file"),
            command=menu_command.new_file
        )
file_menu.add_option(
            option=i18n.t("open_file"),
            command=menu_command.open_file
        )

file_menu.add_separator()

file_menu.add_option(
            option=i18n.t("save"),
            command=menu_command.save_file
        )
file_menu.add_option(
            option=i18n.t("save_as"),
            command=menu_command.save_as_file
        )

file_menu.add_separator()

file_menu.add_option(
            option=i18n.t("settings"),
            command=menu_command.open_theme_setting
        )

file_menu.add_separator()

file_menu.add_option(
            option=i18n.t("exit"),
            command=root.destroy
        )

# Edit
edit_btn = menus.add_cascade(i18n.t("edit"))
edit_menu = CustomDropdownMenu(widget=edit_btn)

edit_menu.add_option(
            option=i18n.t("undo"),
            command=menu_command.undo
        )
edit_menu.add_option(
            option=i18n.t("redo"),
            command=menu_command.redo
        )

edit_menu.add_separator()

edit_menu.add_option(
            option=i18n.t("cut"),
            command=menu_command.cut
        )
edit_menu.add_option(
            option=i18n.t("copy"),
            command=menu_command.copy
        )
edit_menu.add_option(
            option=i18n.t("paste"),
            command=menu_command.paste
        )

edit_menu.add_separator()

edit_menu.add_option(
            option=i18n.t("select_all"),
            command=menu_command.select_all
        )


# View
view_btn = menus.add_cascade(i18n.t("view"))
view_menu = CustomDropdownMenu(widget=view_btn)

view_menu.add_option(
            option=i18n.t("toggle_sidebar"),
            command=menu_command.toggle_sidebar
        )

def apply_language(language: str):
    i18n.set_language(language)
    #// menus.refresh_language()
    sidebar.refresh_language()
    editor.refresh_language()
    root.update_idletasks()

# Sidebar
sidebar = Sidebar(root)
sidebar.pack(side="left", fill="y")

# Recent Bar
right = ctk.CTkFrame(root)
right.pack(side="right", fill="both", expand=True)

# Editor
editor = Editor(right)
editor.pack(fill="both", expand=True)

# Terminal
terminal = Terminal(right)
terminal.pack(fill="x")
editor.set_terminal(terminal)

# Set instances in menu_command for callback
menu_command.set_editor_instance(editor)
menu_command.set_sidebar_instance(sidebar)
setting.set_language_callback(apply_language)


def apply_theme(appearance_mode: str):
    sidebar.apply_theme(appearance_mode)


setting.set_theme_callback(apply_theme)
apply_language(i18n.get_language())

# Define function for opening files from sidebar
def open_file_from_sidebar(file_path, editor_widget, sidebar_widget):
    """Handle file opening from sidebar"""
    if os.path.exists(file_path):
        content = file_manager.load_file_content(file_path)
        file_name = file_manager.get_file_name(file_path)
        editor_widget.set_file_name(file_name)
        editor_widget.set_content(content)
        menu_command.current_file_path = file_path

# Set callback for opening files from sidebar
sidebar.on_file_open = lambda file_path: open_file_from_sidebar(file_path, editor, sidebar)

# Run
root.mainloop()