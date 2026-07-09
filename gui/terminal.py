import customtkinter as ctk


class Terminal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=150)
        self.terminal = ctk.CTkTabview(self)
        self.terminal.pack(fill="both", expand=True, pady=5)

        self.terminal.add("Input")
        self.terminal.add("Output")
        self.terminal.set("Input")

        self.input = ctk.CTkTextbox(self.terminal.tab("Input"), font=("Consolas", 13))
        self.input.pack(fill="both", expand=True, pady=5)

        self.output = ctk.CTkTextbox(self.terminal.tab("Output"), font=("Consolas", 13))
        self.output.pack(fill="both", expand=True, pady=5)
        self.output.configure(state="disabled")

    def clear(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def write(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def get_input_text(self):
        return self.input.get("1.0", "end-1c")

    def clear_input(self):
        self.input.delete("1.0", "end")

    def show_output_tab(self):
        self.terminal.set("Output")