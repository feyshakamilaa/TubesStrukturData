# gui/views_admin/song_table_view.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class SongTableView(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Judul", "Artis", "Genre", "Vibes"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setStyleSheet("""
            QTableWidget {
                background-color:#1a1a1a;
                color:white;
                border-radius:8px;
            }
            QHeaderView::section {
                background-color:#1DB954;
                color:black;
                padding:6px;
                font-weight:bold;
            }
        """)

    def load_songs(self, songs):
        self.setRowCount(len(songs))

        for row, song in enumerate(songs):
            item_judul = QTableWidgetItem(song.judul)
            item_judul.setData(Qt.ItemDataRole.UserRole, song.id) 

            self.setItem(row, 0, item_judul)
            self.setItem(row, 1, QTableWidgetItem(song.artis))
            self.setItem(row, 2, QTableWidgetItem(song.genre))
            self.setItem(row, 3, QTableWidgetItem(song.vibes))