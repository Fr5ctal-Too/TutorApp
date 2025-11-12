import sys
import os

def get_resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', None) # PyInstaller
    if base_path:
        return os.path.join(base_path, relative_path)
    return relative_path
