import os
from PyQt6.QtGui import QIcon

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ICON_DIR = os.path.join(BASE_DIR, "assets", "icons")

def icon(name: str) -> QIcon:
    path = os.path.join(ICON_DIR, f"{name}.svg")
    return QIcon(path)