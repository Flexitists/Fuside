import customtkinter as ctk
import json
import os

class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200)

        sidebar = ctk.CTkFrame(self, width=250)
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(sidebar, text="Recently Opened").pack(anchor="w", padx=10)
        
        self.recent_frame = ctk.CTkScrollableFrame(sidebar)
        self.recent_frame.pack(fill="both", expand=True, padx=10,)
        
        # Load recent files from JSON
        self.recent_files = self.load_recent_files()
        self.display_recent_files(self.recent_frame)
        
        # Footer frame for warning and delete all button
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(anchor="w", padx=10, pady=(5, 10))
        
        #ctk.CTkLabel(footer_frame, text="This is an internal test version.", text_color="red").pack(side="left")
        
        delete_all_btn = ctk.CTkButton(
            footer_frame,
            text="✕ Delete all",
            width=70,
            height=20,
            font=("Arial", 9),
            fg_color="red",
            hover_color="darkred",
            command=self.delete_all_files
        )
        delete_all_btn.pack(side="right", padx=(5, 0))
        
        self.editor = None
        self.on_file_open = None
    
    def load_recent_files(self):
        """Load recent files from assents/recent_files.json"""
        json_path = os.path.join(os.path.dirname(__file__), "..", "assents", "recent_files.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("recent_files", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def display_recent_files(self, parent_frame):
        """Display recent files as buttons in the frame"""
        for file_path in self.recent_files:
            file_name = os.path.basename(file_path)
            
            # Create a frame for each file row
            file_row = ctk.CTkFrame(parent_frame, fg_color="transparent")
            file_row.pack(fill="x", padx=5, pady=2)
            
            # Open button
            btn = ctk.CTkButton(
                file_row, 
                text=f"{file_name[:20] + "..." if len(file_name) > 20 else file_name}",
                anchor="w",
                fg_color="transparent",
                hover_color="gray20",
                command=lambda f=file_path: self.open_file(f)
            )
            btn.pack(side="left", fill="x", expand=True)
            
            # Delete button
            del_btn = ctk.CTkButton(
                file_row,
                text="✕",
                width=25,
                height=25,
                fg_color="transparent",
                hover_color="red",
                text_color="gray",
                command=lambda f=file_path: self.delete_file(f)
            )
            del_btn.pack(side="right", padx=5)
    
    def refresh_recent_files(self):
        """Refresh the sidebar with updated recent files"""
        # Clear the frame
        for widget in self.recent_frame.winfo_children():
            widget.destroy()
        
        # Reload recent files
        self.recent_files = self.load_recent_files()
        
        # Display updated files
        self.display_recent_files(self.recent_frame)
    
    def open_file(self, file_path):
        """Handle file opening"""
        if os.path.exists(file_path) and self.on_file_open:
            self.on_file_open(file_path)
    
    def delete_file(self, file_path):
        """Delete file from recent list"""
        from core import file_manager
        
        file_manager.delete_from_recent_files(file_path)
        self.refresh_recent_files()
    
    def delete_all_files(self):
        """Delete all recent files"""
        from core import file_manager
        
        file_manager.delete_all_recent_files()
        self.refresh_recent_files()


        