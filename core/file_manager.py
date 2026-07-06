import os

from core import setting


def add_to_recent_files(file_path):
    """Add file to recent files list in settings"""
    setting.add_to_recent_files(file_path)


def delete_from_recent_files(file_path):
    """Delete file from recent files list"""
    setting.delete_from_recent_files(file_path)


def delete_all_recent_files():
    """Delete all recent files"""
    setting.delete_all_recent_files()


def load_file_content(file_path):
    """Load content from file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def get_file_name(file_path):
    """Get file name from path"""
    return os.path.basename(file_path)

