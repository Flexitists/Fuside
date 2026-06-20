import customtkinter as ctk

class Editor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # ---------------- Khu vực 1: Thanh chứa tên file và nút Run (Top) ----------------
        name_and_run_frame = ctk.CTkFrame(self)
        name_and_run_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.name_file = ctk.CTkLabel(name_and_run_frame, text="Untitled", font=("Arial", 13, "bold"))
        self.name_file.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        run_button = ctk.CTkButton(name_and_run_frame, text="▶ Run", width=80, height=28)
        run_button.pack(side="right", padx=5, pady=5)

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
        self.editor.configure(spacing1=2)

        # 3. Lắng nghe các sự kiện gõ phím, cuộn chuột để cập nhật và đồng bộ số dòng
        self.editor.bind("<KeyRelease>", self.update_line_numbers)
        self.editor.bind("<MouseWheel>", self.sync_scroll)
        self.editor.bind("<Button-1>", self.update_line_numbers) 
        self.editor.bind("<B1-Motion>", self.sync_scroll) # Đồng bộ khi bôi đen text kéo chuột lên/xuống

        # Phím tắt thủ công cho Undo/Redo
        self.editor.bind("<Control-z>", self._undo)
        self.editor.bind("<Control-y>", self._redo)
    
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
    
    def set_content(self, content):
        """Xóa nội dung cũ và nạp nội dung mới vào editor"""
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.update_line_numbers() # Cập nhật lại bộ đếm dòng ngay lập tức
    
    def set_file_name(self, file_name):
        """Cập nhật nhãn tên file"""
        self.name_file.configure(text=file_name)
    
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