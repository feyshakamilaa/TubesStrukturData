# gui/admin_window.py
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QApplication, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from controllers.shared import get_song_controller
from structures.song import Song

from gui.views_admin.song_table_view import SongTableView
from gui.views_admin.song_editor_dialog import SongEditorDialog
from gui.views_admin.delete_confirm_dialog import confirm_delete
from gui.icons import icon


class AdminWindow(QMainWindow):
    def __init__(self, user_window_ref=None, login_window_ref=None):
        super().__init__()
        self.setWindowTitle("Admin Panel Musik")
        self.setGeometry(150, 80, 1000, 700)

        self.song_controller = get_song_controller()
        self.user_window_ref = user_window_ref
        self.login_window_ref = login_window_ref

        root = QWidget()
        layout = QVBoxLayout(root)

        # HEADER
        header = QHBoxLayout()
        title = QLabel("GoSic Admin")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))

        btn_logout = QPushButton("Logout")
        btn_logout.setIcon(icon("logout"))
        btn_logout.setProperty("buttonRole", "outline-danger")
        btn_logout.clicked.connect(self._logout)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_logout)
        layout.addLayout(header)

        # TABEL LAGU
        self.table = SongTableView()
        layout.addWidget(self.table)

        # TOMBOL CRUD
        controls = QHBoxLayout()
        controls.setSpacing(10)

        btn_add = QPushButton("Add Music")
        btn_add.setIcon(icon("add_circle"))
        btn_add.setProperty("buttonRole", "primary")

        btn_edit = QPushButton("Edit Music")
        btn_edit.setIcon(icon("edit"))
        btn_edit.setProperty("buttonRole", "secondary")

        btn_delete = QPushButton("Delete Music")
        btn_delete.setIcon(icon("delete_forever"))
        btn_delete.setProperty("buttonRole", "danger")

        btn_add.clicked.connect(self._add_song)
        btn_edit.clicked.connect(self._edit_song)
        btn_delete.clicked.connect(self._delete_song)

        controls.addWidget(btn_add)
        controls.addWidget(btn_edit)
        controls.addWidget(btn_delete)
        controls.addStretch()

        layout.addLayout(controls)

        self.setCentralWidget(root)
        self.refresh_table()

    def refresh_table(self, keep_song_id=None):
        songs = self.song_controller.get_all_songs()
        self.table.load_songs(songs)

        if keep_song_id:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item.data(Qt.ItemDataRole.UserRole) == keep_song_id:
                    self.table.selectRow(row)
                    break

    # ADD SONG
    def _add_song(self):
        dialog = SongEditorDialog(self, mode="add")
        if dialog.exec():
            data = dialog.get_data()
            if data:
                judul, artis, genre, vibes, file_path, cover_path = data
                self.song_controller.add_song(
                    Song(judul, artis, genre, vibes, file_path, cover_path)
                )
                self.refresh_table()

                # realtime ke user
                if self.user_window_ref:
                    self.user_window_ref.refresh_current_view()

    # EDIT SONG
    def _edit_song(self):
        song_id = self._get_selected_song_id()
        if not song_id:
            QMessageBox.warning(self, "Error", "Select a song.")
            return

        song = self.song_controller.find_song_by_id(song_id)
        dialog = SongEditorDialog(self, mode="edit", song=song)

        if dialog.exec():
            data = dialog.get_data()
            if data:
                judul, artis, genre, vibes, file_path, cover_path = data
                self.song_controller.update_song(song_id, judul, artis, genre, vibes, file_path, cover_path)
                self.refresh_table(keep_song_id=song_id)

    def _get_selected_song_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole)

    # DELETE SONG
    def _delete_song(self):
        song_id = self._get_selected_song_id()
        if not song_id:
            QMessageBox.warning(self, "Error", "Select a song.")
            return

        if confirm_delete(self):
            self.song_controller.delete_song_by_id(song_id)
            self.refresh_table()

    # LOGOUT
    def _logout(self):
        if self.login_window_ref:
            self.close()
            self.login_window_ref.show()
        else:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    win = AdminWindow()
    win.show()
    sys.exit(app.exec())