# gui/views/favorites_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel,
    QPushButton, QHBoxLayout, QDialog, QListWidget, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap

from structures.song import Song


class FavoriteCard(QFrame):
    """
    Kartu besar untuk lagu favorit (modern Spotify-Tech)
    Dengan fitur:
    - Play
    - Add to Queue
    - Add to Playlist
    - Remove Favorite (♥)
    """
    def __init__(self, parent_window, song: Song):
        super().__init__()

        self.parent_window = parent_window
        self.song = song

        self.setFixedSize(290, 280)
        self.setStyleSheet("""
            QFrame {
                background-color:#1E1E1E;
                border-radius:18px;
            }
            QFrame:hover {
                background-color:#262626;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Cover (placeholder)
        cover = QLabel()
        cover.setFixedSize(260, 150)
        cover.setScaledContents(True)

        if song.cover_path:
            cover.setPixmap(QPixmap(song.cover_path))
        else:
            cover.setStyleSheet("""
                background-color:#313137;
                border-radius:14px;
                border:1px solid #3A5256;
            """)
        layout.addWidget(cover, alignment=Qt.AlignmentFlag.AlignCenter)

        # Title
        lbl_title = QLabel(song.judul)
        lbl_title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        layout.addWidget(lbl_title)

        # Artist
        lbl_artist = QLabel(song.artis)
        lbl_artist.setStyleSheet("color:#ABAAA5; font-size:12px;")
        layout.addWidget(lbl_artist)

        # BUTTON ROW
        row = QHBoxLayout()
        row.setSpacing(8)

        # PLAY
        btn_play = QPushButton("Play")
        btn_play.setFixedSize(70, 40)
        btn_play.setStyleSheet("""
            QPushButton {
                background-color:#F92D44;
                color:white;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover { background-color:#ff4d63; }
        """)
        btn_play.clicked.connect(lambda _, s=song: parent_window._play_song_from_card(s))
        row.addWidget(btn_play)

        # ADD TO QUEUE
        btn_queue = QPushButton("Queue")
        btn_queue.setFixedSize(70, 40)
        btn_queue.setStyleSheet("""
            QPushButton {
                background-color:#3A5256;
                color:white;
                border-radius:10px;
            }
            QPushButton:hover { background-color:#4f6a6e; }
        """)
        btn_queue.clicked.connect(lambda _, s=song: parent_window.add_to_queue(s))
        row.addWidget(btn_queue)

        # ADD TO PLAYLIST
        btn_add_pl = QPushButton("Playlist")
        btn_add_pl.setFixedSize(80, 40)
        btn_add_pl.setStyleSheet("""
            QPushButton {
                background-color:#ABAAA5;
                color:#000;
                border-radius:10px;
            }
            QPushButton:hover { background-color:#bfbeb8; }
        """)
        btn_add_pl.clicked.connect(self._add_to_playlist_dialog)
        row.addWidget(btn_add_pl)

        layout.addLayout(row)

        # REMOVE FAVORITE (♥)
        btn_unfav = QPushButton("♥")
        btn_unfav.setFixedSize(34, 34)
        btn_unfav.setStyleSheet("""
            QPushButton {
                background:transparent;
                color:#F92D44;
                font-size:22px;
                border:none;
            }
            QPushButton:hover { color:#ff6278; }
        """)

        btn_unfav.clicked.connect(self._remove_favorite)

        # Align right
        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(btn_unfav)
        layout.addLayout(bottom)

    # REMOVE FAVORITE
    def _remove_favorite(self):
        self.parent_window.remove_favorite(self.song)
        self.parent_window._show_favorites_view()

    # ADD TO PLAYLIST (dialog pilih playlist)
    def _add_to_playlist_dialog(self):
        playlists = list(self.parent_window.playlists.keys())
        if not playlists:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Playlist", "There are no playlists yet.")
            return

        dialog = QDialog()
        dialog.setWindowTitle("Select Playlist")
        dialog.setFixedSize(300, 400)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for p in playlists:
            list_widget.addItem(p)
        layout.addWidget(list_widget)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            idx = list_widget.currentRow()
            if idx < 0:
                return
            playlist_name = playlists[idx]
            self.parent_window.add_song_to_playlist(playlist_name)
            self.parent_window._show_favorites_view()


class FavoritesView(QWidget):
    """
    Menampilkan daftar lagu favorit dalam bentuk grid 3 kolom
    """
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(14)

        fav_songs = parent_window.get_favorite_songs()

        if not fav_songs:
            empty = QLabel("There are no favorite songs yet.\nClick the ♥ icon on the song.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color:#ABAAA5; font-size:15px;")
            root.addWidget(empty)
            return

        grid = QGridLayout()
        grid.setSpacing(18)

        MAX_COL = 3
        row = col = 0

        for s in fav_songs:
            card = FavoriteCard(parent_window, s)
            grid.addWidget(card, row, col)
            col += 1
            if col >= MAX_COL:
                col = 0
                row += 1

        root.addLayout(grid)