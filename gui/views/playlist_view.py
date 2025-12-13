# gui/views/playlist_view.py
from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap

from structures.double_linked_list import DoubleLinkedList
from gui.icons import icon


class PlaylistView(QWidget):
    """
    Tampilan daftar playlist dalam bentuk grid (kartu)
    """
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window

        grid = QGridLayout(self)
        grid.setSpacing(20)
        grid.setContentsMargins(10, 10, 10, 10)

        MAX_COL = 3
        row = col = 0

        playlists = parent_window.playlists.items()

        if not playlists:
            empty = QLabel("There are no playlists yet.\nCreate a new playlist to get started!")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color:#ABAAA5; font-size:16px;")
            grid.addWidget(empty, 0, 0)
            return

        for name, dll in playlists:
            card = self._create_playlist_card(name, dll)
            grid.addWidget(card, row, col)

            col += 1
            if col >= MAX_COL:
                col = 0
                row += 1

    # CARD PLAYLIST
    def _create_playlist_card(self, name: str, dll: DoubleLinkedList):
        card = QFrame()
        card.setFixedSize(280, 360)
        card.setStyleSheet("""
            QFrame {
                background-color:#1E1E1E;
                border-radius:16px;
            }
            QFrame:hover {
                background-color:#262626;
            }
        """)

        v = QVBoxLayout(card)
        v.setContentsMargins(14, 14, 14, 14)
        v.setSpacing(12)

        # COVER PLAYLIST (GAMBAR)
        cover = QLabel()
        cover.setFixedSize(240, 180)
        cover.setScaledContents(True)

        cover_path = self.parent_window.playlist_covers.get(name)

        if cover_path:
            cover.setPixmap(QPixmap(cover_path))
        else:
            cover.setPixmap(QPixmap("assets/cover/playlist_default.png"))

        v.addWidget(cover, alignment=Qt.AlignmentFlag.AlignCenter)

        # TITLE
        lbl_title = QLabel(name)
        lbl_title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        v.addWidget(lbl_title)

        # COUNT
        lbl_count = QLabel(f"{dll.size} lagu")
        lbl_count.setStyleSheet("color:#ABAAA5; font-size:12px;")
        v.addWidget(lbl_count)

        # BUTTONS
        btn_grid = QGridLayout()
        btn_grid.setSpacing(10)

        # PLAY playlist
        btn_play = QPushButton("Play")
        btn_play.setIcon(icon("play_arrow"))
        btn_play.setIconSize(QSize(16, 16))
        btn_play.setProperty("buttonRole", "primary")
        btn_play.clicked.connect(lambda _, d=dll: self.parent_window._play_playlist_first(d))
        btn_play.setFixedHeight(34)
        btn_grid.addWidget(btn_play, 0, 0)

        # LIHAT DETAIL
        btn_view = QPushButton("See Music")
        btn_view.setIcon(icon("visibility"))
        btn_view.setIconSize(QSize(16, 16))
        btn_view.setProperty("buttonRole", "secondary")
        btn_view.clicked.connect(lambda _, n=name: self.parent_window.open_playlist_detail(n))
        btn_view.setFixedHeight(34)
        btn_grid.addWidget(btn_view, 0, 1)

        # EDIT NAMA
        btn_edit = QPushButton("Edit")
        btn_edit.setIcon(icon("edit"))
        btn_edit.setIconSize(QSize(16, 16))
        btn_edit.setProperty("buttonRole", "secondary")
        btn_edit.clicked.connect(lambda _, old=name: self._edit_playlist_name(old))
        btn_edit.setFixedHeight(34)
        btn_grid.addWidget(btn_edit, 1, 0)

        # HAPUS
        btn_delete = QPushButton("Hapus")
        btn_delete.setIcon(icon("delete"))
        btn_delete.setIconSize(QSize(16, 16))
        btn_delete.setProperty("buttonRole", "danger")
        btn_delete.clicked.connect(lambda _, nm=name: self._delete_playlist(nm))
        btn_delete.setFixedHeight(34)
        btn_grid.addWidget(btn_delete, 1, 1)

        v.addLayout(btn_grid)

        return card

    # EDIT / DELETE
    def _edit_playlist_name(self, old_name):
        from PyQt6.QtWidgets import QInputDialog
        new_name, ok = QInputDialog.getText(self, "Edit Playlist", "Nama baru:")
        if ok and new_name.strip():
            self.parent_window.rename_playlist(old_name, new_name.strip())

    def _delete_playlist(self, name):
        from PyQt6.QtWidgets import QMessageBox
        confirm = QMessageBox.question(
            self,
            "Hapus Playlist",
            f"Yakin ingin menghapus playlist '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.parent_window.delete_playlist(name)