# gui/views/queue_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QHBoxLayout, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from gui.icons import icon
from structures.song import Song
from structures.queue import Queue


class QueueListWidget(QListWidget):
    """QListWidget dengan drag-drop internal dan tampilan halus."""

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSpacing(10)

        self.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                margin-top: 8px;
                margin-bottom: 8px;
            }
        """)

        # LIST MENGISI SEMUA RUANG
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def dropEvent(self, event):
        super().dropEvent(event)
        self.parent_view.update_queue_order()


class QueueView(QWidget):
    """Antrian lagu dengan drag & drop serta full-height layout."""

    def __init__(self, parent_window, queue: Queue):
        super().__init__()
        self.parent_window = parent_window
        self.queue = queue

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(16)

        # CASE: EMPTY
        if queue.is_empty():
            empty = QLabel("Queue is empty.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color:#ABAAA5; font-size:14px;")
            main.addWidget(empty)
            return

        # LIST WIDGET FULL HEIGHT
        self.list_widget = QueueListWidget(self)
        self.list_widget.setMinimumHeight(400)  
        main.addWidget(self.list_widget, stretch=1)

        # LOAD QUEUE ITEMS WITHOUT DESTROYING ORDER
        temp = []
        while not queue.is_empty():
            s = queue.dequeue()
            temp.append(s)

        for s in temp:
            queue.enqueue(s)
            self._add_song_item(s)

    def _add_song_item(self, song: Song):
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 90))

        frame = QFrame()
        frame.setProperty("song_id", song.id)
        frame.setStyleSheet("""
            QFrame {
                background-color:#262629;
                border-radius:16px;
            }
            QFrame:hover {
                background-color:#303033;
            }
        """)
        h = QHBoxLayout(frame)
        h.setContentsMargins(14, 14, 14, 14)
        h.setSpacing(14)

        # PLAY BUTTON
        btn_play = QPushButton()
        btn_play.setIcon(icon("play_arrow"))
        btn_play.setIconSize(QSize(22, 22))
        btn_play.setFixedSize(48, 48)
        btn_play.setProperty("buttonRole", "primary")
        btn_play.clicked.connect(lambda _, s=song: self._play(s))
        h.addWidget(btn_play)

        # TITLE + ARTIST
        info = QVBoxLayout()
        lbl_title = QLabel(song.judul)
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color:white;")

        lbl_artist = QLabel(song.artis)
        lbl_artist.setStyleSheet("color:#ABAAA5; font-size:12px;")

        info.addWidget(lbl_title)
        info.addWidget(lbl_artist)
        h.addLayout(info, stretch=1)

        # DELETE BUTTON
        btn_del = QPushButton()
        btn_del.setIcon(icon("delete"))
        btn_del.setIconSize(QSize(20, 20))
        btn_del.setFixedSize(48, 48)
        btn_del.setProperty("buttonRole", "danger")
        btn_del.clicked.connect(lambda _, s=song: self._remove(s))
        h.addWidget(btn_del)

        # APPLY
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, frame)

    def _play(self, song: Song):
        self.parent_window._play_song(song)
        self.parent_window._show_queue_view()

    def _remove(self, song: Song):
        """Remove satu item dari queue dan refresh view."""
        new_q = Queue()
        removed = False

        while not self.queue.is_empty():
            s = self.queue.dequeue()
            if s == song and not removed:
                removed = True
                continue
            new_q.enqueue(s)

        self.parent_window.queue = new_q
        self.parent_window._show_queue_view()

    def update_queue_order(self):
        """Update queue sesuai hasil drag & drop."""
        new_q = Queue()

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)

            labels = widget.findChildren(QLabel)
            judul = labels[0].text()
            artis = labels[1].text()

            song_id = widget.property("song_id")
            song = self.parent_window.controller.find_song_by_id(song_id)
            if song:
                new_q.enqueue(song)

        self.parent_window.queue = new_q