import customtkinter as ctk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

from core import i18n

class Editor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # ---------------- Khu vực 1: Thanh chứa tên file và nút Run (Top) ----------------
        name_and_run_frame = ctk.CTkFrame(self)
        name_and_run_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.name_file = ctk.CTkLabel(name_and_run_frame, text=i18n.t("untitled"), font=("Arial", 13, "bold"))
        self.name_file.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.run_button = ctk.CTkButton(name_and_run_frame, text=f"▶ {i18n.t('run')}", width=80, height=28)
        self.run_button.pack(side="right", padx=5, pady=5)

        # ---------------- Khu vực 2: Khung chứa nội dung Editor & Số dòng (Bottom) ----------------
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(side="bottom", fill="both", expand=True)

        # Cấu hình grid hệ thống cho content_frame: cột 1 (editor) sẽ tự giãn rộng ra
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # 1. Khởi tạo ô hiển thị số dòng (Line Numbers) - Đặt font Monospace cố định
        self.line_numbers = ctk.CTkTextbox(
            content_frame, 
            width=45, 
            text_color="gray", 
            fg_color="transparent", 
            activate_scrollbars=False,   # Tắt thanh cuộn riêng biệt
            font=("Consolas", 13)        # Cần chung font và cỡ chữ với editor
        )
        self.line_numbers.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.line_numbers.configure(spacing1=2) 
        self.line_numbers.insert("1.0", "1")
        self.line_numbers.configure(state="disabled") # Khóa không cho người dùng sửa số dòng

        # 2. Khởi tạo ô nhập code chính (Editor)
        self.editor = ctk.CTkTextbox(
            content_frame, 
            undo=True,                   # Kích hoạt tính năng undo/redo tích hợp sẵn của Tkinter
            font=("Consolas", 13)        # Dùng font chữ đồng bộ với cột số dòng
        )
        self.editor.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.editor.configure(spacing1=2, tabs=("32",))

        # Setup syntax highlighting for Python
        self.syntax_lexer = PythonLexer()
        self.syntax_tag_specs = [
            (Token.Comment,"#6A9955", "#6A9955"),
            (Token.Keyword, "py_keyword", "#569CD6"),
            (Token.Name.Builtin, "py_builtin", "#4EC9B0"),
            (Token.Name.Function, "py_function", "#DCDCAA"),
            (Token.Name.Class, "py_class", "#4EC9B0"),
            (Token.Literal.String, "py_string", "#CE9178"),
            (Token.Literal.Number, "py_number", "#B5CEA8"),
            (Token.Operator, "py_operator", "#D4D4D4"),
            (Token.Punctuation, "py_punctuation", "#D4D4D4"),
            (Token.Name.Namespace, "py_namespace", "#4EC9B0"),
            (Token.Name.Decorator, "#C586C0", "#C586C0"),
            (Token.Text, "py_text", "#D4D4D4"),
        ]
        self._setup_syntax_tags()
        self.syntax_after_id = None

        # 3. Lắng nghe các sự kiện gõ phím, cuộn chuột để cập nhật và đồng bộ số dòng
        self.editor.bind("<KeyRelease>", self.on_text_change)
        self.editor.bind("<MouseWheel>", self.sync_scroll)
        self.editor.bind("<Button-1>", self.update_line_numbers) 
        self.editor.bind("<B1-Motion>", self.sync_scroll) # Đồng bộ khi bôi đen text kéo chuột lên/xuống

        # Phím tắt thủ công cho Undo/Redo
        self.editor.bind("<Control-z>", self._undo)
        self.editor.bind("<Control-y>", self._redo)

        self.editor.bind("<Control-x>", lambda e: self.editor.event_generate("<<Cut>>"))
        self.editor.bind("<Control-c>", lambda e: self.editor.event_generate("<<Copy>>"))
        self.editor.bind("<Control-v>", lambda e: self.editor.event_generate("<<Paste>>"))
    
    def _undo(self, event=None):
        """Hành động Undo"""
        try:
            self.editor.edit_undo()
            self.update_line_numbers() # Cập nhật lại số dòng sau khi undo
        except:
            pass
        return "break"
    
    def _redo(self, event=None):
        """Hành động Redo"""
        try:
            self.editor.edit_redo()
            self.update_line_numbers() # Cập nhật lại số dòng sau khi redo
        except:
            pass
        return "break"
    
    def _setup_syntax_tags(self):
        for _, tag_name, color in self.syntax_tag_specs:
            self.editor.tag_config(tag_name, foreground=color)

    def on_text_change(self, event=None):
        self.update_line_numbers()
        self.schedule_syntax_highlight()

    def schedule_syntax_highlight(self):
        if self.syntax_after_id:
            self.after_cancel(self.syntax_after_id)
        self.syntax_after_id = self.after(100, self.highlight_python_syntax)

    def highlight_python_syntax(self):
        self.syntax_after_id = None
        code = self.editor.get("1.0", "end-1c")
        for _, tag_name, _ in self.syntax_tag_specs:
            self.editor.tag_remove(tag_name, "1.0", "end")

        if not code:
            return

        row = 1
        col = 0
        for token_type, token_value in lex(code, self.syntax_lexer):
            if not token_value:
                continue

            start_index = f"{row}.{col}"
            for ch in token_value:
                if ch == "\n":
                    row += 1
                    col = 0
                else:
                    col += 1
            end_index = f"{row}.{col}"

            for token_class, tag_name, _ in self.syntax_tag_specs:
                if token_type in token_class:
                    self.editor.tag_add(tag_name, start_index, end_index)
                    break

    def set_content(self, content):
        """Xóa nội dung cũ và nạp nội dung mới vào editor"""
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.update_line_numbers() # Cập nhật lại bộ đếm dòng ngay lập tức
        self.highlight_python_syntax()
    
    def set_file_name(self, file_name):
        """Cập nhật nhãn tên file"""
        self.name_file.configure(text=file_name)

    def refresh_language(self):
        self.name_file.configure(text=i18n.t("untitled") if self.name_file.cget("text") == "Untitled" else self.name_file.cget("text"))
        self.run_button.configure(text=f"▶ {i18n.t('run')}")
    
    def get_content(self):
        """Lấy toàn bộ text hiện tại từ editor"""
        return self.editor.get("1.0", "end-1c")

    def update_line_numbers(self, event=None):
        """Cập nhật lại số lượng dòng dựa trên nội dung bên ô nhập code"""
        final_index = self.editor.index("end-1c")
        num_lines = int(final_index.split(".")[0])

        # Tạo chuỗi số dòng dạng "1\n2\n3\n..."
        lines_string = "\n".join(str(i) for i in range(1, num_lines + 1))

        # Cập nhật văn bản vào ô chứa số dòng
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", lines_string)
        self.line_numbers.configure(state="disabled")
        
        # Đồng bộ vị trí cuộn
        self.sync_scroll()

    def sync_scroll(self, event=None):
        """Đồng bộ vị trí cuộn dọc (yview) của ô số dòng khớp với ô nhập code"""
        top_visible_index = self.editor.yview()
        self.line_numbers.yview_moveto(top_visible_index[0])


# ---- Đoạn code Test chạy thử giao diện ----
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("700idx", "500")
    root.geometry("800x500")
    root.title("Fuside IDE")
    
    editor_widget = Editor(root)
    editor_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    root.mainloop()