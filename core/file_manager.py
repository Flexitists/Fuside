import json
import os
from datetime import datetime

def add_to_recent_files(file_path):
    """Add file to recent files list in JSON"""
    json_path = os.path.join(os.path.dirname(__file__), "..", "assents", "recent_files.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"recent_files": []}
    
    recent_files = data.get("recent_files", [])
    
    # Remove if already exists
    if file_path in recent_files:
        recent_files.remove(file_path)
    
    # Add to beginning
    recent_files.insert(0, file_path)
    
    # Keep only last 10 files
    recent_files = recent_files[:10]
    
    data["recent_files"] = recent_files
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def delete_from_recent_files(file_path):
    """Delete file from recent files list"""
    json_path = os.path.join(os.path.dirname(__file__), "..", "assents", "recent_files.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    recent_files = data.get("recent_files", [])
    
    # Remove the file if it exists
    if file_path in recent_files:
        recent_files.remove(file_path)
    
    data["recent_files"] = recent_files
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def delete_all_recent_files():
    """Delete all recent files"""
    json_path = os.path.join(os.path.dirname(__file__), "..", "assents", "recent_files.json")
    
    data = {"recent_files": []}
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

