import customtkinter as ctk

class Terminal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=150)

        terminal_label = ctk.CTkLabel(self, text="Terminal")
        terminal_label.pack(side="top")

        terminal = ctk.CTkTextbox(self, font=("Consolas", 13))
        terminal.pack(fill="both", expand=True, pady=5)