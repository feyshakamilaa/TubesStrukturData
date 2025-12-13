# gui/login_window.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from controllers.auth import check_login
from gui.icons import icon


class LoginPopup(QFrame):
    """
    Modern card login panel
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginCard")
        self.setFixedSize(430, 380)

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(45)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(Qt.GlobalColor.black)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(38, 32, 38, 32)
        layout.setSpacing(20)

        # Logo di atas
        logo = QLabel()
        logo.setPixmap(icon("library_music").pixmap(40, 40))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        # Title
        title = QLabel("GoSic Login")
        title.setObjectName("LoginTitle")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Go Music")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #ABAAA5;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Helper buat input dengan ikon
        def make_row(placeholder: str, icon_name: str):
            row = QHBoxLayout()
            row.setSpacing(10)

            lbl_icon = QLabel()
            lbl_icon.setPixmap(icon(icon_name).pixmap(18, 18))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(lbl_icon)

            box = QLineEdit()
            box.setPlaceholderText(placeholder)
            row.addWidget(box, 1)
            return row, box

        # Username
        row_user, self.username_input = make_row("Username", "person")
        layout.addLayout(row_user)

        # Password
        row_pass, self.password_input = make_row("Password", "lock")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addLayout(row_pass)

        # LOGIN BUTTON
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("LoginButton")
        self.login_button.setProperty("buttonRole", "primary")
        self.login_button.setFixedHeight(46)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.login_button)
        btn_row.addStretch()
        layout.addLayout(btn_row)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 900, 650)

        # referensi window
        self.user_window = None
        self.admin_window = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        center = QHBoxLayout()
        center.addStretch()
        self.popup = LoginPopup()
        center.addWidget(self.popup)
        center.addStretch()

        root.addStretch()
        root.addLayout(center)
        root.addStretch()

        # Close button kecil
        self.close_btn = QPushButton("×", self)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setProperty("buttonRole", "outline-danger")
        self.close_btn.clicked.connect(self.close)

        # Aksi login
        self.popup.login_button.clicked.connect(self.do_login)
        self.popup.password_input.returnPressed.connect(self.do_login)
        self.popup.username_input.returnPressed.connect(self.do_login)

    def resizeEvent(self, event):
        # Letak tombol X relatif ke card
        px = (self.width() - self.popup.width()) // 2
        py = (self.height() - self.popup.height()) // 2
        self.close_btn.move(px + self.popup.width() - 12, py - 18)
        super().resizeEvent(event)

    def do_login(self):
        username = self.popup.username_input.text()
        password = self.popup.password_input.text()

        role = check_login(username, password)

        if role is None:
            QMessageBox.warning(self, "Login Failed", "Username or password is incorrect!!")
            return

        if role == "admin":
            from gui.admin_window import AdminWindow
            if self.admin_window is None:
                self.admin_window = AdminWindow(
                    user_window_ref=self.user_window,
                    login_window_ref=self
                )
            else:
                self.admin_window.user_window_ref = self.user_window
                self.admin_window.login_window_ref = self
            self.win = self.admin_window
        else:
            from gui.user_window import UserWindow
            if self.user_window is None:
                self.user_window = UserWindow(login_window_ref=self)
            self.win = self.user_window

        self.win.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    w = LoginWindow()
    w.show()
    sys.exit(app.exec())