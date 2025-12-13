from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QGridLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap

from gui.icons import icon
from structures.song import Song


class SongCard(QFrame):
    """
    Full-bleed Spotify-style Song Card
    + Favorite (♥ / ♡)
    + Remove button (ONLY in playlist)
    """
    def __init__(self, parent_window, song: Song, in_playlist=False):
        super().__init__()
        self.parent_window = parent_window
        self.song = song
        self.in_playlist = in_playlist

        self.setFixedSize(280, 300)
        self.setStyleSheet("""
            QFrame {
                background-color: #2B2B2E;
                border-radius: 22px;
            }
            QFrame:hover {
                background-color: #323234;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # COVER IMAGE
        cover = QLabel()
        cover.setFixedSize(252, 150)
        cover.setScaledContents(True)

        if song.cover_path:
            pixmap = QPixmap(song.cover_path)
            cover.setPixmap(pixmap)
        else:
            cover.setStyleSheet("""
                background-color:#323234;
                border-radius:18px;
                border:1px solid #3A5256;
            """)
        layout.addWidget(cover, alignment=Qt.AlignmentFlag.AlignCenter)

        # TITLE
        lbl_title = QLabel(song.judul)
        lbl_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(lbl_title)

        # ARTIST
        lbl_artist = QLabel(song.artis)
        lbl_artist.setStyleSheet("color:#ABAAA5; font-size:12px;")
        layout.addWidget(lbl_artist)

        # BUTTON ROW (Play + Queue)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_play = QPushButton("Play")
        btn_play.setIcon(icon("play_arrow"))
        btn_play.setIconSize(QSize(16, 16))
        btn_play.setProperty("buttonRole", "primary")
        btn_play.setFixedHeight(34)
        btn_play.clicked.connect(
            lambda _, s=song: parent_window._play_song_from_card(s)
        )
        btn_row.addWidget(btn_play)

        btn_queue = QPushButton("Antrian")
        btn_queue.setIcon(icon("add"))
        btn_queue.setIconSize(QSize(16, 16))
        btn_queue.setProperty("buttonRole", "secondary")
        btn_queue.setFixedHeight(34)
        btn_queue.clicked.connect(
            lambda _, s=song: parent_window.add_to_queue(s)
        )
        btn_row.addWidget(btn_queue)

        layout.addLayout(btn_row)

        # FAVORITE + REMOVE ROW
        fav_layout = QHBoxLayout()

        # REMOVE (ONLY IN PLAYLIST)
        if self.in_playlist:
            btn_remove = QPushButton("Hapus")
            btn_remove.setIcon(icon("delete"))
            btn_remove.setProperty("buttonRole", "danger")
            btn_remove.setFixedHeight(32)
            btn_remove.clicked.connect(self._remove_from_playlist)
            fav_layout.addWidget(btn_remove)

        fav_layout.addStretch()

        # FAVORITE BUTTON
        self.btn_fav = QPushButton()
        self.btn_fav.setFixedSize(40, 36)
        self.btn_fav.setStyleSheet(
            "border:none; background:transparent; font-size:20px;"
        )

        self._update_fav_ui()
        self.btn_fav.clicked.connect(self._toggle_fav)

        fav_layout.addWidget(self.btn_fav)
        layout.addLayout(fav_layout)

        self.setMouseTracking(True)

    # =====================================================
    # FAVORITE HANDLER
    # =====================================================
    def _is_favorite(self):
        return self.song.id in self.parent_window.favorites

    def _update_fav_ui(self):
        if self._is_favorite():
            self.btn_fav.setText("♥")
            self.btn_fav.setStyleSheet(
                "color:#F92D44; font-size:20px; border:none; background:transparent;"
            )
        else:
            self.btn_fav.setText("♡")
            self.btn_fav.setStyleSheet(
                "color:#ABAAA5; font-size:20px; border:none; background:transparent;"
            )

    def _toggle_fav(self):
        self.parent_window.toggle_favorite(self.song)
        self._update_fav_ui()

    # =====================================================
    # REMOVE FROM PLAYLIST (SAFE)
    # =====================================================
    def _remove_from_playlist(self):
        if hasattr(self.parent_window, "remove_song_from_current_playlist"):
            self.parent_window.remove_song_from_current_playlist(self.song)


# ============================================================
# GRID VIEW (3 columns)
# ============================================================

class SongGridView(QWidget):
    def __init__(self, parent_window, songs: list[Song], in_playlist=False):
        super().__init__()
        self.parent_window = parent_window
        self.songs = songs
        self.in_playlist = in_playlist

        grid = QGridLayout(self)
        grid.setSpacing(18)
        grid.setContentsMargins(10, 10, 10, 10)

        MAX_COL = 3
        row = col = 0

        for song in songs:
            card = SongCard(
                parent_window,
                song,
                in_playlist=self.in_playlist
            )
            grid.addWidget(card, row, col)

            col += 1
            if col >= MAX_COL:
                col = 0
                row += 1