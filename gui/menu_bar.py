from CTkMenuBar import *
from core import menu_command, i18n

class Menu(CTkTitleMenu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self._build_menu()

    def _build_menu(self):
        self._clear_menu()

        # File
        file_btn = self.add_cascade(i18n.t("file"))

        self.file_menu = CustomDropdownMenu(widget=file_btn)
        #// file_btn.bind("<Button-1>", lambda e: self.file_menu.toggleShow())

        self.file_menu.add_option(
            option=i18n.t("new_file"),
            command=menu_command.new_file
        )

        self.file_menu.add_option(
            option=i18n.t("open_file"),
            command=menu_command.open_file
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option=i18n.t("save"),
            command=menu_command.save_file
        )

        self.file_menu.add_option(
            option=i18n.t("save_as"),
            command=menu_command.save_as_file
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option=i18n.t("settings"),
            command=menu_command.open_theme_setting
        )

        self.file_menu.add_separator()

        self.file_menu.add_option(
            option=i18n.t("exit"),
            command=self.master.destroy
        )

        # Edit
        edit_btn = self.add_cascade(i18n.t("edit"))

        self.edit_menu = CustomDropdownMenu(widget=edit_btn)
        #// edit_btn.bind("<Button-1>", lambda e: self.edit_menu.toggleShow())

        self.edit_menu.add_option(
            option=i18n.t("undo"),
            command=menu_command.undo
        )

        self.edit_menu.add_option(
            option=i18n.t("redo"),
            command=menu_command.redo
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option=i18n.t("cut"),
            command=menu_command.cut
        )

        self.edit_menu.add_option(
            option=i18n.t("copy"),
            command=menu_command.copy
        )

        self.edit_menu.add_option(
            option=i18n.t("paste"),
            command=menu_command.paste
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option=i18n.t("select_all"),
            command=menu_command.select_all
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_option(
            option=i18n.t("find"),
            command=menu_command.find
        )

        self.edit_menu.add_option(
            option=i18n.t("replace"),
            command=menu_command.replace
        )

        # View
        view_btn = self.add_cascade(i18n.t("view"))

        #// view_btn.bind("<Button-1>", lambda e: self.view_menu.toggleShow())
        self.view_menu = CustomDropdownMenu(widget=view_btn)

        self.view_menu.add_option(
            option=i18n.t("toggle_sidebar"),
            command=menu_command.toggle_sidebar
        )

    def refresh_language(self):
        self._build_menu()

    def _clear_menu(self):
        for child in self.winfo_children():
            child.destroy()
