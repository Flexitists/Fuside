from CTkMenuBar import *
from core import menu_command

class Menu(CTkTitleMenu):
    def __init__(self, master):
        super().__init__(master)

        # File
        file_btn = self.add_cascade("File")

        self.file_menu = CustomDropdownMenu(widget=file_btn)
        #// file_btn.bind("<Button-1>", lambda e: self.file_menu.toggleShow())

        self.file_menu.add_option(
            option="New File",
            command=menu_command.new_file
        )

        self.file_menu.add_option(
            option="Open File...",
            command=menu_command.open_file
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option="Save",
            command=menu_command.save_file
        )

        self.file_menu.add_option(
            option="Save As...",
            command=menu_command.save_as_file
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option="Settings",
            command=menu_command.open_theme_setting
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option="Exit",
            command=master.destroy
        )

        # Edit
        edit_btn = self.add_cascade("Edit")

        self.edit_menu = CustomDropdownMenu(widget=edit_btn)
        #// edit_btn.bind("<Button-1>", lambda e: self.edit_menu.toggleShow())

        self.edit_menu.add_option(
            option="Undo",
            command=menu_command.undo
        )

        self.edit_menu.add_option(
            option="Redo",
            command=menu_command.redo
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option="Cut",
            command=menu_command.cut
        )

        self.edit_menu.add_option(
            option="Copy",
            command=menu_command.copy
        )

        self.edit_menu.add_option(
            option="Paste",
            command=menu_command.paste
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option="Select All",
            command=menu_command.select_all
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option="Find",
            command=menu_command.find
        )

        self.edit_menu.add_option(
            option="Replace",
            command=menu_command.replace
        )

        # View
        view_btn = self.add_cascade("View")

        #// view_btn.bind("<Button-1>", lambda e: self.view_menu.toggleShow())
        self.view_menu = CustomDropdownMenu(widget=view_btn)

        self.view_menu.add_option(
            option="Toggle Sidebar",
            command=menu_command.toggle_sidebar
        )
