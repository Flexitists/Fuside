import customtkinter as ctk
import os, json
from tkinter import messagebox

with open(os.path.join(os.path.dirname(__file__) , ".." ,  "assents", "theme.json"), "r") as theme_config:
    data = json.load(theme_config)
    ctk.set_appearance_mode(data["theme_appearance"])
    ctk.set_default_color_theme(data["theme_color"])

def save_setting():
    data["theme_appearance"] = appearance_set.get()
    data["theme_color"] = color_set.get()
    with open(os.path.join(os.path.dirname(__file__) , ".." ,  "assents", "theme.json"), "w") as theme_config:
        json.dump(data, theme_config)
    messagebox.showinfo("Applied!", "Restart Fuside to change the interface!")

app = ctk.CTk()
app.title("Theme Setting")
app.iconbitmap(os.path.join(os.path.dirname(__file__), "..", "assents", "icon.ico"))
app.resizable(False, False)

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", padx=20, pady=20)

appearance_label = ctk.CTkLabel(main_frame, text="   Appearance")
appearance_label.grid(column=0, row=0)
appearance_set = ctk.CTkSegmentedButton(main_frame, values=["System","Light","Dark"])
appearance_set.set(data["theme_appearance"])
appearance_set.grid(column=1, row=0)

ctk.CTkLabel(main_frame, text="").grid(column=0, row=1)

color_label = ctk.CTkLabel(main_frame, text="Color       ")
color_label.grid(column=0, row=2)
color_set = ctk.CTkSegmentedButton(main_frame, values=["blue","green","dark-blue"])
color_set.set(data["theme_color"])
color_set.grid(column=1, row=2)

ctk.CTkLabel(main_frame, text="").grid(column=0, row=3)

save_button = ctk.CTkButton(main_frame, text="Apply", command=save_setting)
save_button.grid(column=1, row=4)

app.mainloop()