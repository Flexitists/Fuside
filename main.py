import customtkinter as ctk
import os

from gui.terminal import Terminal
from gui.editor import Editor
from gui.menu_bar import Menu
from gui.recent_bar import Sidebar
from core import menu_command, file_manager, setting, i18n

# Load theme configuration from shared settings
appearance, color = setting.get_theme_settings()
ctk.set_appearance_mode(appearance)
ctk.set_default_color_theme(color)


root = ctk.CTk()
root.title("Fuside")
root.iconbitmap(os.path.join(os.path.dirname(__file__), "assets", "icon.ico"))
root.geometry("1000x625")

# Menu - pass theme data to ensure synchronization
menus = Menu(root)


def apply_language(language: str):
    i18n.set_language(language)
    menus.refresh_language()
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

# Set instances in menu_command for callback
menu_command.set_editor_instance(editor)
menu_command.set_sidebar_instance(sidebar)
setting.set_language_callback(apply_language)
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