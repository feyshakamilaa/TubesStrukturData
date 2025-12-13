# gui/dialogs/add_song_playlist_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QListWidget, QListWidgetItem,
    QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt

class AddSongPlaylistDialog(QDialog):
    def __init__(self, songs):
        super().__init__()
        self.setWindowTitle("Tambah Lagu ke Playlist")
        self.selected_songs = []

        layout = QVBoxLayout(self)

        self.list = QListWidget()
        self.list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        for song in songs:
            item = QListWidgetItem(f"{song.judul} - {song.artis}")
            item.setData(Qt.ItemDataRole.UserRole, song)
            self.list.addItem(item)

        layout.addWidget(self.list)

        btn_add = QPushButton("Tambah")
        btn_add.clicked.connect(self._save)
        layout.addWidget(btn_add)

    def _save(self):
        for item in self.list.selectedItems():
            self.selected_songs.append(
                item.data(Qt.ItemDataRole.UserRole)
            )
        self.accept()
