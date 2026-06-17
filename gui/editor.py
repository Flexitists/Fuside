import customtkinter as ctk

class Editor(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #Name file and run button
        name_and_run_frame = ctk.CTkFrame(self)
        name_and_run_frame.pack(fill="both")

        self.name_file = ctk.CTkLabel(name_and_run_frame, text="Untitled")
        self.name_file.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        run_button = ctk.CTkButton(name_and_run_frame, text="▶ Run", width=80, height=28)
        run_button.pack(side="right", padx=5, pady=5)

        #Editor with undo/redo enabled
        self.editor = ctk.CTkTextbox(self)
        self.editor.pack(fill="both", expand=True)
        
        # Enable undo/redo support
        self.editor.bind("<Control-z>", self._undo)
        self.editor.bind("<Control-y>", self._redo)
    
    def _undo(self, event=None):
        """Undo action"""
        try:
            self.editor.edit_undo()
        except:
            pass
        return "break"
    
    def _redo(self, event=None):
        """Redo action"""
        try:
            self.editor.edit_redo()
        except:
            pass
        return "break"
    
    def set_content(self, content):
        """Clear editor and set new content"""
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
    
    def set_file_name(self, file_name):
        """Update file name label"""
        self.name_file.configure(text=file_name)
    
    def get_content(self):
        """Get current editor content"""
        return self.editor.get("1.0", "end-1c")
