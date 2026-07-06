from tkinter import TclError, filedialog, messagebox
from core import file_manager
import os
import subprocess

# Global references to editor and sidebar
editor_instance = None
sidebar_instance = None
current_file_path = None

def set_editor_instance(editor):
    """Set editor instance for use in menu commands"""
    global editor_instance
    editor_instance = editor

def set_sidebar_instance(sidebar):
    """Set sidebar instance for use in menu commands"""
    global sidebar_instance
    sidebar_instance = sidebar

def new_file():
    """Create a new file"""
    global current_file_path
    current_file_path = None
    if editor_instance:
        editor_instance.set_file_name("Untitled")
        editor_instance.set_content("")

def open_file():
    """Open a file"""
    global current_file_path
    file_path = filedialog.askopenfilename(
        title="Open",
        filetypes=[
            ("Python Files", "*.py"),
            ("C Files","*.c"),
            ("C++ Files", "*.cpp"),
            ("Pascal Files","*.pas"),
            ("All Files","*.*")
        ]
    )

    if file_path:
        # Read file content
        content = file_manager.load_file_content(file_path)
        current_file_path = file_path
        
        # Add to recent files
        file_manager.add_to_recent_files(file_path)
        
        # Update editor
        if editor_instance:
            file_name = file_manager.get_file_name(file_path)
            editor_instance.set_file_name(file_name)
            editor_instance.set_content(content)
        
        # Update sidebar
        if sidebar_instance:
            sidebar_instance.refresh_recent_files()

def save_file():
    """Save current file"""
    global current_file_path
    
    if current_file_path is None:
        save_as_file()
        return
    
    if editor_instance:
        content = editor_instance.get_content()
        try:
            with open(current_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def save_as_file():
    """Save file with a new name"""
    global current_file_path
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[
            ("Python Files", "*.py"),
            ("C Files","*.c"),
            ("C++ Files", "*.cpp"),
            ("Pascal Files","*.pas"),
            ("All Files","*.*")
        ]
    )
    
    if file_path:
        if editor_instance:
            content = editor_instance.get_content()
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                current_file_path = file_path
                file_manager.add_to_recent_files(file_path)
                editor_instance.set_file_name(file_manager.get_file_name(file_path))
                if sidebar_instance:
                    sidebar_instance.refresh_recent_files()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def open_theme_setting():
    """Open theme setting window"""
    from core.setting import open_settings

    if editor_instance and editor_instance.winfo_toplevel():
        open_settings(editor_instance.winfo_toplevel())
    else:
        open_settings()

# Edit menu functions
def undo():
    """Undo action"""
    if editor_instance:
        try:
            editor_instance.editor.edit_undo()
        except:
            messagebox.showinfo("Info", "Nothing to undo")

def redo():
    """Redo action"""
    if editor_instance:
        try:
            editor_instance.editor.edit_redo()
        except:
            messagebox.showinfo("Info", "Nothing to redo")

def cut():
    """Cut selected text"""
    if editor_instance:
        try:
            selected_text = editor_instance.editor.get("sel.first", "sel.last")
            editor_instance.editor.clipboard_clear()
            editor_instance.editor.clipboard_append(selected_text)
            editor_instance.editor.delete("sel.first", "sel.last")
            editor_instance.editor.focus_set()
            editor_instance.update_line_numbers()
        except TclError:
            pass

def copy():
    """Copy selected text"""
    if editor_instance:
        try:
            selected_text = editor_instance.editor.get("sel.first", "sel.last")
            editor_instance.editor.clipboard_clear()
            editor_instance.editor.clipboard_append(selected_text)
            editor_instance.editor.focus_set()
        except TclError:
            pass

def paste():
    """Paste text"""
    if editor_instance:
        try:
            clipboard_text = editor_instance.editor.clipboard_get()
            try:
                editor_instance.editor.delete("sel.first", "sel.last")
            except TclError:
                pass
            editor_instance.editor.insert("insert", clipboard_text)
            editor_instance.editor.focus_set()
            editor_instance.update_line_numbers()
        except TclError:
            pass

def select_all():
    """Select all text"""
    if editor_instance:
        editor_instance.editor.focus_set()
        editor_instance.editor.tag_remove("sel", "1.0", "end")
        editor_instance.editor.tag_add("sel", "1.0", "end-1c")
        editor_instance.editor.mark_set("insert", "1.0")
        editor_instance.editor.see("insert")
        return "break"

def find():
    """Find text in editor"""
    if editor_instance:
        find_window = filedialog.askstring("Find", "Enter text to find:")
        if find_window:
            content = editor_instance.get_content()
            if find_window in content:
                idx = content.find(find_window)
                editor_instance.editor.tag_add("found", f"1.0+{idx}c", f"1.0+{idx+len(find_window)}c")
                editor_instance.editor.tag_config("found", background="yellow")
                messagebox.showinfo("Found", f"Text found at position {idx}")
            else:
                messagebox.showinfo("Not Found", "Text not found")

def replace():
    """Replace text in editor"""
    if editor_instance:
        find_text = filedialog.askstring("Replace", "Find:")
        if find_text:
            replace_text = filedialog.askstring("Replace", "Replace with:")
            if replace_text is not None:
                content = editor_instance.get_content()
                new_content = content.replace(find_text, replace_text)
                editor_instance.set_content(new_content)
                messagebox.showinfo("Success", "Replace completed")

# View menu functions
def toggle_sidebar():
    """Toggle sidebar visibility"""
    if sidebar_instance:
        if sidebar_instance.winfo_viewable():
            sidebar_instance.pack_forget()
        else:
            sidebar_instance.pack(side="left", fill="y")

