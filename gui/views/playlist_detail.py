from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFrame, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from gui.views.song_card import SongGridView
from structures.double_linked_list import DoubleLinkedList
from gui.dialogs.add_song_playlist_dialog import AddSongPlaylistDialog


class PlaylistDetailView(QWidget):
    """
    Menampilkan isi sebuah playlist dalam bentuk GRID (ala Spotify)
    + tombol Tambah Lagu yang jelas & multi-select
    + MODE PLAYLIST AKTIF (in_playlist=True)
    """

    def __init__(self, parent_window, playlist_name: str, dll: DoubleLinkedList):
        super().__init__()
        self.parent_window = parent_window
        self.playlist_name = playlist_name
        self.dll = dll

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(14)

        # TITLE
        lbl_title = QLabel(f"Playlist: {playlist_name}")
        lbl_title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: white;")
        layout.addWidget(lbl_title)

        # ACTION BAR (TAMBAH LAGU)
        action_bar = QFrame()
        action_bar.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(10, 6, 10, 6)

        btn_add = QPushButton("+ Tambah Lagu")
        btn_add.setFixedHeight(42)
        btn_add.setMinimumWidth(200)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        btn_add.clicked.connect(self._add_many_songs)

        action_layout.addStretch()
        action_layout.addWidget(btn_add)
        action_layout.addStretch()

        layout.addWidget(action_bar)

        # Hint kecil (UX)
        hint = QLabel("Pilih satu atau lebih lagu untuk ditambahkan ke playlist")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("color:#AAAAAA; font-size:11px;")
        layout.addWidget(hint)

        # GRID LAGU (MODE PLAYLIST AKTIF)
        self.grid_view = SongGridView(
            parent_window,
            self.dll.to_list(),
            in_playlist=True   
        )
        layout.addWidget(self.grid_view)

    # TAMBAH BANYAK LAGU KE PLAYLIST (MULTI SELECT)
    def _add_many_songs(self):
        dialog = AddSongPlaylistDialog(
            self.parent_window.controller.get_all_songs()
        )

        if dialog.exec():
            for song in dialog.selected_songs:
                self.dll.add_last(song)

            self.refresh()

    # REFRESH GRID (BUAT ULANG VIEW)
    def refresh(self):
        # hapus grid lama
        self.grid_view.setParent(None)

        # buat ulang grid dengan data terbaru (MODE PLAYLIST TETAP AKTIF)
        self.grid_view = SongGridView(
            self.parent_window,
            self.dll.to_list(),
            in_playlist=True  
        )

        # tambahkan kembali ke layout
        self.layout().addWidget(self.grid_view)