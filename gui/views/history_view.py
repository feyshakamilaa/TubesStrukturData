# gui/views/history_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt6.QtGui import QFont, QPixmap  
from PyQt6.QtCore import Qt

from structures.stack import Stack
from structures.song import Song


class HistoryListItem(QFrame):
    def __init__(self, parent_window, song: Song, is_favorited=False):
        super().__init__()

        self.parent_window = parent_window
        self.song = song

        self.setStyleSheet("""
            QFrame {
                background-color:#1E1E1E;
                border-radius:12px;
            }
            QFrame:hover {
                background-color:#262626;
            }
        """)
        self.setFixedHeight(90)

        h = QHBoxLayout(self)
        h.setContentsMargins(12, 10, 12, 10)
        h.setSpacing(16)

        # Thumbnail
        thumb = QLabel()
        thumb.setFixedSize(64, 64)
        thumb.setScaledContents(True)

        if song.cover_path:
            thumb.setPixmap(QPixmap(song.cover_path))
        else:
            thumb.setStyleSheet("""
                background-color:#313137;
                border-radius:8px;
                border: 1px solid #3A5256;
            """)

        h.addWidget(thumb)

        # Judul + Artis
        text_box = QVBoxLayout()
        lbl_title = QLabel(song.judul)
        lbl_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        lbl_artist = QLabel(song.artis)
        lbl_artist.setStyleSheet("color:#ABAAA5; font-size:12px;")

        text_box.addWidget(lbl_title)
        text_box.addWidget(lbl_artist)
        h.addLayout(text_box)
        h.addStretch()

        # ACTION BUTTONS
        action_box = QHBoxLayout()
        action_box.setSpacing(8)

        # FAVORITE BUTTON ♥ / ♡
        self.btn_fav = QPushButton()
        self.btn_fav.setFixedSize(38, 38)
        self.btn_fav.setStyleSheet("border:none; background:transparent; font-size:22px;")

        if is_favorited:
            self.btn_fav.setText("♥")
            self.btn_fav.setStyleSheet("color:#F92D44; border:none; background:transparent; font-size:22px;")
        else:
            self.btn_fav.setText("♡")
            self.btn_fav.setStyleSheet("color:#ABAAA5; border:none; background:transparent; font-size:22px;")

        def toggle():
            state = self.parent_window.toggle_favorite(song)
            if state:
                self.btn_fav.setText("♥")
                self.btn_fav.setStyleSheet("color:#F92D44; border:none; background:transparent; font-size:22px;")
            else:
                self.btn_fav.setText("♡")
                self.btn_fav.setStyleSheet("color:#ABAAA5; border:none; background:transparent; font-size:22px;")

        self.btn_fav.clicked.connect(toggle)
        action_box.addWidget(self.btn_fav)

        # ADD TO QUEUE BUTTON
        btn_add = QPushButton("＋")
        btn_add.setFixedSize(38, 38)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color:#3A5256;
                color:white;
                font-size:18px;
                border-radius:8px;
            }
            QPushButton:hover {
                background-color:#4f6c70;
            }
        """)
        btn_add.clicked.connect(lambda _, s=song: self.parent_window.add_to_queue(s))
        action_box.addWidget(btn_add)

        # PLAY BUTTON
        btn_play = QPushButton("▶")
        btn_play.setFixedSize(40, 40)
        btn_play.setStyleSheet("""
            QPushButton {
                background-color:#F92D44;
                color:white;
                font-size:18px;
                border-radius:8px;
            }
            QPushButton:hover {
                background-color:#ff5c70;
            }
        """)
        btn_play.clicked.connect(lambda _, s=song: self.parent_window._play_song_from_card(s))
        action_box.addWidget(btn_play)

        h.addLayout(action_box)


class HistoryView(QWidget):
    """
    Menampilkan riwayat lagu (Stack) dalam bentuk list elegan modern
    (tanpa judul double—title sudah di UserWindow)
    """
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        # Copy stack
        temp = Stack()
        songs = []

        while not self.parent_window.history.is_empty():
            s = self.parent_window.history.pop()
            songs.append(s)
            temp.push(s)

        # Kembalikan isi stack
        while not temp.is_empty():
            self.parent_window.history.push(temp.pop())

        # Empty state
        if not songs:
            empty = QLabel("No songs have been played yet.")
            empty.setStyleSheet("color:#ABAAA5; font-size:15px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty)
            return

        # Tampilkan lagu terbaru paling atas
        for s in songs[::-1]:
            key = (s.judul, s.artis)
            is_fav = key in self.parent_window.favorites
            item = HistoryListItem(parent_window, s, is_favorited=is_fav)
            layout.addWidget(item)

        layout.addStretch()