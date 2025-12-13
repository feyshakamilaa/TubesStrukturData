# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load 
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("style.qss tidak ditemukan! Pastikan file ada di folder yang sama dengan main.py.")

    win = LoginWindow()
    win.show()

    sys.exit(app.exec())