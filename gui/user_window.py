# gui/user_window.py
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QFrame, QScrollArea, QApplication, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

from controllers.shared import get_song_controller
from structures.double_linked_list import DoubleLinkedList
from structures.stack import Stack
from structures.queue import Queue
from structures.song import Song
from structures.multi_linked_list import MultiLinkedList

from gui.views.playlist_view import PlaylistView
from gui.views.playlist_detail import PlaylistDetailView
from gui.views.queue_view import QueueView
from gui.views.favorites_view import FavoritesView
from gui.views.history_view import HistoryView
from gui.views.song_card import SongGridView
from gui.icons import icon

class UserWindow(QWidget):
    def __init__(self, login_window_ref=None):
        super().__init__()
        self.login_window_ref = login_window_ref
        self.setWindowTitle("Music Player - User")
        self.setGeometry(120, 60, 1200, 780)

        # controller (shared)
        self.controller = get_song_controller()

        # Data structures
        self.playlist = DoubleLinkedList()
        self.queue = Queue()
        self.history = Stack()
        self.favorites = set()
        self.is_playing = False
        self.vibe_mll = MultiLinkedList()
        
        # Inisialisasi player audio
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)   # 50% volume

        # Load all songs awal ke playlist utama
        all_songs = self.controller.get_all_songs()
        for s in all_songs:
            self.playlist.add_last(s)
            self.vibe_mll.add_song(s)
        self.playlist.current = None

        # Named playlists
        self.playlists: dict[str, DoubleLinkedList] = {}
        self.playlist_covers: dict[str, str] = {}   # namenya path cover

        # View state
        self.current_view_name = "all_songs"
        self.viewing_playlist_name: str | None = None

        # ROOT LAYOUT
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = self._sidebar()
        root.addWidget(self.sidebar)

        # Content container
        self.content_container = QFrame()
        content_vbox = QVBoxLayout(self.content_container)
        content_vbox.setContentsMargins(18, 18, 18, 10)
        content_vbox.setSpacing(10)

        self.header = self._create_header_bar()
        self.title_bar = self._create_title_bar()
        self.main_area = self._create_main_area()
        self.player_bar = self._player_bar()

        content_vbox.addWidget(self.header)
        content_vbox.addWidget(self.title_bar)
        content_vbox.addWidget(self.main_area, 1)
        content_vbox.addWidget(self.player_bar, 0)

        root.addWidget(self.content_container, 1)

        # Default: langsung ke All Songs (Home)
        self._show_all_songs()

    # SIDEBAR
    def _sidebar(self):
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(220)

        v = QVBoxLayout(frame)
        v.setContentsMargins(18, 18, 14, 18)
        v.setSpacing(10)

        title = QLabel("MUSIC")
        title.setObjectName("SidebarTitle")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        v.addWidget(title)

        items = [
            ("Home", "home", self._action_home),
            ("Search", "search", self._action_search),
            ("Playlist", "playlist", self._action_playlist),
            ("Queue", "queue_music", self._action_queue),            
            ("Favorites", "favorite", self._action_favorites),
            ("History", "history", self._action_history),
        ]
        for text, icon_name, func in items:
            btn = QPushButton(text)
            btn.setIcon(icon(icon_name))
            btn.setIconSize(QSize(18, 18))
            btn.setProperty("role", "sidebar")
            btn.clicked.connect(func)
            v.addWidget(btn)

        v.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("LogoutButton")
        logout_btn.setIcon(icon("logout"))
        logout_btn.setIconSize(QSize(18, 18))
        logout_btn.clicked.connect(self._action_logout)
        v.addWidget(logout_btn)

        return frame

    # HEADER BAR
    def _create_header_bar(self):
        header = QFrame()
        header.setObjectName("HeaderBar")
        h = QHBoxLayout(header)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(10)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search for music, artists, or playlists...")
        self.search.setMinimumHeight(42)
        self.search.textChanged.connect(self._on_search_text)
        h.addWidget(self.search)

        return header

    # TITLE BAR
    def _create_title_bar(self):
        bar = QFrame()
        h = QHBoxLayout(bar)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)

        self.title_lbl = QLabel("All Songs")
        self.title_lbl.setObjectName("PageTitle")
        self.title_lbl.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        h.addWidget(self.title_lbl)

        h.addStretch()

        self.create_btn = QPushButton("Create Playlist")
        self.create_btn.setProperty("buttonRole", "primary")
        self.create_btn.setFixedHeight(34)
        self.create_btn.clicked.connect(self._create_playlist)
        h.addWidget(self.create_btn)

        self.back_btn = QPushButton("Back")
        self.back_btn.setProperty("buttonRole", "secondary")
        self.back_btn.setFixedHeight(34)
        self.back_btn.clicked.connect(self._back_from_detail)
        self.back_btn.hide()
        h.addWidget(self.back_btn)

        return bar

    # MAIN AREA
    def _create_main_area(self):
        container = QFrame()
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border:none;")

        self._current_view_widget = QWidget()
        self.scroll.setWidget(self._current_view_widget)

        v.addWidget(self.scroll)
        return container

    def _set_central_widget(self, widget: QWidget, view_name: str):
        self._current_view_widget.setParent(None)
        self._current_view_widget = widget
        self.scroll.setWidget(self._current_view_widget)
        self.current_view_name = view_name

    # PLAYER BAR
    def _player_bar(self):
        bar = QFrame()
        bar.setObjectName("PlayerBar")
        bar.setFixedHeight(90)

        h = QHBoxLayout(bar)
        h.setContentsMargins(20, 12, 20, 12)
        h.setSpacing(14)

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(icon("skip_previous"))
        self.btn_prev.setIconSize(QSize(22, 22))
        self.btn_prev.setProperty("role", "player-secondary")

        self.btn_play = QPushButton()
        self.btn_play.setIcon(icon("play_arrow"))
        self.btn_play.setIconSize(QSize(26, 26))
        self.btn_play.setProperty("role", "player-main")

        self.btn_next = QPushButton()
        self.btn_next.setIcon(icon("skip_next"))
        self.btn_next.setIconSize(QSize(22, 22))
        self.btn_next.setProperty("role", "player-secondary")

        for b in (self.btn_prev, self.btn_play, self.btn_next):
            b.setFixedSize(48, 48)

        self.btn_prev.clicked.connect(self._prev)
        self.btn_play.clicked.connect(self._play_or_pause)
        self.btn_next.clicked.connect(self._next)

        self.lbl_now = QLabel("No song is playing")
        self.lbl_now.setFont(QFont("Segoe UI", 12))

        h.addWidget(self.btn_prev)
        h.addWidget(self.btn_play)
        h.addWidget(self.btn_next)
        h.addSpacing(20)
        h.addWidget(self.lbl_now)
        h.addStretch()

        return bar

    # VIEW SWITCHING
    def _show_all_songs(self):
        self.title_lbl.setText("All Songs")
        self.create_btn.hide()
        self.back_btn.hide()
        self.viewing_playlist_name = "All Songs"

        songs = self.controller.get_all_songs()
        view = SongGridView(parent_window=self, songs=songs)
        self._set_central_widget(view, "all_songs")

    def _show_playlist_view(self):
        self.title_lbl.setText("Playlist")
        self.create_btn.show()
        self.back_btn.hide()
        self.viewing_playlist_name = None

        view = PlaylistView(parent_window=self)
        self._set_central_widget(view, "playlists")

    def _show_playlist_detail(self, name: str, dll: DoubleLinkedList):
        self.title_lbl.setText(name)
        self.create_btn.hide()
        self.back_btn.show()
        self.viewing_playlist_name = name

        view = PlaylistDetailView(parent_window=self, playlist_name=name, dll=dll)
        self._set_central_widget(view, "playlist_detail")

    def _show_queue_view(self):
        self.title_lbl.setText("Queue")
        self.create_btn.hide()
        self.back_btn.show()
        view = QueueView(parent_window=self, queue=self.queue)
        self._set_central_widget(view, "queue")

    def _show_favorites_view(self):
        self.title_lbl.setText("Favorite Song")
        self.create_btn.hide()
        self.back_btn.show()
        view = FavoritesView(parent_window=self)
        self._set_central_widget(view, "favorites")

    def _show_history_view(self):
        self.title_lbl.setText("Playback History")
        self.create_btn.hide()
        self.back_btn.show()
        view = HistoryView(parent_window=self)
        self._set_central_widget(view, "history")

    def _show_search_results(self, text: str):
        songs = self.controller.search(text)
        self.title_lbl.setText(f"Search: {text}")
        self.create_btn.hide()
        self.back_btn.show()
        view = SongGridView(parent_window=self, songs=songs)
        self._set_central_widget(view, "search")

    # SEARCH HANDLER
    def _on_search_text(self, text: str):
        text = text.strip()
        if text == "":
            # kembali ke view sebelumnya
            if self.current_view_name in ("search", "all_songs"):
                self._show_all_songs()
            elif self.current_view_name == "playlist_detail":
                if self.viewing_playlist_name == "All Songs" or not self.viewing_playlist_name:
                    self._show_all_songs()
                elif self.viewing_playlist_name in self.playlists:
                    dll = self.playlists[self.viewing_playlist_name]
                    self._show_playlist_detail(self.viewing_playlist_name, dll)
                else:
                    self._show_playlist_view()
            else:
                self._show_playlist_view()
            return

        self._show_search_results(text)

    # SIDEBAR ACTIONS
    def _action_home(self):
        self._show_all_songs()

    def _action_search(self):
        self.search.setFocus()

    def _action_playlist(self):
        self._show_playlist_view()

    def _action_queue(self):
        self._show_queue_view()

    def _action_favorites(self):
        self._show_favorites_view()

    def _action_history(self):
        self._show_history_view()

    # PLAYLIST CRUD
    def _create_playlist(self):
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QLabel

        class CreatePlaylistDialog(QDialog):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Buat Playlist Baru")
                self.setFixedSize(320, 180)
                v = QVBoxLayout(self)
                lbl = QLabel("Playlist Name:")
                self.edit = QLineEdit()
                self.edit.setPlaceholderText("Enter a playlist name...")
                buttons = QDialogButtonBox(
                    QDialogButtonBox.StandardButton.Ok |
                    QDialogButtonBox.StandardButton.Cancel
                )
                buttons.accepted.connect(self.accept)
                buttons.rejected.connect(self.reject)
                v.addWidget(lbl)
                v.addWidget(self.edit)
                v.addWidget(buttons)

            def get_name(self):
                return self.edit.text().strip()

        dialog = CreatePlaylistDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_name()
            if not name:
                QMessageBox.warning(self, "Failed", "The playlist name cannot be empty.")
                return
            if name in self.playlists:
                QMessageBox.warning(self, "Failed", "A playlist with this name already exists.")
                return

            self.playlists[name] = DoubleLinkedList()
            cover_path, _ = QFileDialog.getOpenFileName(
                self,
                "Pilih Cover Playlist",
                "",
                "Image Files (*.png *.jpg *.jpeg)"
            )
            if cover_path:
                self.playlist_covers[name] = cover_path

            QMessageBox.information(self, "Playlist Created", f"Playlist '{name}' has been created!")
            self._show_playlist_view()

    def rename_playlist(self, old_name: str, new_name: str):
        if new_name in self.playlists:
            QMessageBox.warning(self, "Failed", "A playlist with this name already exists.")
            return False
        self.playlists[new_name] = self.playlists.pop(old_name)
        if old_name in self.playlist_covers:
            self.playlist_covers[new_name] = self.playlist_covers.pop(old_name)
        if self.viewing_playlist_name == old_name:
            self.viewing_playlist_name = new_name
        QMessageBox.information(self, "Berhasil", "Playlist berhasil diubah.")
        self._show_playlist_view()
        return True

    def remove_song_from_current_playlist(self, song):
        name = self.viewing_playlist_name
        if not name or name not in self.playlists:
            return

        dll = self.playlists[name]

        removed = dll.remove(song)

        if removed:
            QMessageBox.information(
                self,
                "Deleted",
                f"Music '{song.judul}' removed from playlist."
            )

        # refresh tampilan playlist
        self._show_playlist_detail(name, dll)


    def delete_playlist(self, name: str):
        if name in self.playlists:
            self.playlists.pop(name)

        if name in self.playlist_covers:
            self.playlist_covers.pop(name)

        QMessageBox.information(self, "Dihapus", "Playlist berhasil dihapus.")
        self._show_playlist_view()

    def open_playlist_detail(self, name: str):
        dll = self.playlists.get(name)
        if dll:
            self._show_playlist_detail(name, dll)

    def add_song_to_playlist(self, playlist_name: str):
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QListWidget

        songs = self.controller.get_all_songs()
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Add Music to {playlist_name}")
        dialog.setFixedSize(400, 500)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for s in songs:
            list_widget.addItem(f"{s.judul} - {s.artis}")
        layout.addWidget(list_widget)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = list_widget.currentRow()
            if selected < 0:
                QMessageBox.warning(self, "Failed", "Please select a song first.")
                return

            song = songs[selected]
            self.playlists[playlist_name].add_last(song)

            QMessageBox.information(self, "Succeed", f"Music '{song.judul}' added.")
            self._show_playlist_view()

    # FAVORITES
    def toggle_favorite(self, song):
        key = song.id

        # sudah favorit maka hapus
        if key in self.favorites:
            self.favorites.remove(key)
            return False

        # belum favorit maka tambah
        self.favorites.add(key)
        return True


    def get_favorite_songs(self):
        fav_list = []
        for song_id in self.favorites:
            s = self.controller.find_song_by_id(song_id)

            if s:
                fav_list.append(s)
        return fav_list


    def remove_favorite(self, song):
        key = song.id
        if key in self.favorites:
            self.favorites.remove(key)

    # QUEUE & HISTORY HELPERS
    def add_to_queue(self, song: Song, show_message=True):
        self.queue.enqueue(song)
        if show_message:
            QMessageBox.information(self, "Queue", f"'{song.judul}' added to queue.")

    def record_history(self, song: Song):
        self.history.push(song)

    # PLAYBACK
    def _play_playlist_first(self, dll: DoubleLinkedList):
        if dll.size == 0:
            QMessageBox.information(self, "Kosong", "Playlist kosong.")
            return

        self.playlist.clear()
        for s in dll.to_list():
            self.playlist.add_last(s)

        first = self.playlist.play_first()
        if first:
            self._play_song(first)

    def _play_song_from_card(self, song: Song):
        self._play_song(song)

        # Jika ada di queue, hapus
        temp = Queue()
        removed = False
        while not self.queue.is_empty():
            s = self.queue.dequeue()
            if s == song and not removed:
                removed = True
                continue
            temp.enqueue(s)
        self.queue = temp


    def _play_song(self, song: Song):
        # rekam history
        self.record_history(song)
        self.is_playing = True
        self.btn_play.setIcon(icon("pause"))
        self.lbl_now.setText(f"Now Playing: {song.judul} - {song.artis}")

        # arahkan DLL playlist ke lagu ini
        node = self.playlist.jump_to_song(song)
        if not node:
            self.playlist.add_last(song)
            self.playlist.current = self.playlist.tail

        # === PEMUTARAN AUDIO ===
        if song.file_path:
            self.player.setSource(QUrl.fromLocalFile(song.file_path))
            self.player.play()

    def _play_or_pause(self):
        if not self.playlist.current:
            first = self.playlist.play_first()
            if first:
                self._play_song(first)
            return

        if self.is_playing:
            self.player.pause()
            cur = self.playlist.current.data
            self.lbl_now.setText(f"Paused: {cur.judul}")
            self.btn_play.setIcon(icon("play_arrow"))
            self.is_playing = False
        else:
            self.player.play()
            cur = self.playlist.current.data
            self.lbl_now.setText(f"Now Playing: {cur.judul} - {cur.artis}")
            self.btn_play.setIcon(icon("pause"))
            self.is_playing = True

    def _next(self):
        # 1. Prioritas ANTRIAN dulu
        if not self.queue.is_empty():
            next_song = self.queue.dequeue()
            self._play_song(next_song)
            if self.current_view_name == "queue":
                self._show_queue_view()
            return

        # 2. Jika BUKAN di HOME, maka playlist navigation
        if self.current_view_name != "all_songs":
            nxt = self.playlist.next_song()
            if nxt:
                self._play_song(nxt)
            else:
                QMessageBox.information(self, "Info", "There is no next song.")
            return

        # 3. HOME MODE: berdasarkan Vibe dulu
        if self.playlist.current:
            current_song = self.playlist.current.data
            vibe_next = self.controller.get_next_same_vibe(current_song)

            if vibe_next:
                self._play_song(vibe_next)
                return

        # 4. FALLBACK memakai DLL (All Songs)
        nxt = self.playlist.next_song()
        if nxt:
            self._play_song(nxt)
        else:
            QMessageBox.information(self, "Info", "There is no next song.")

    def _prev(self):
        # playlist mode maka DLL biasa
        if self.current_view_name != "all_songs":
            prev = self.playlist.prev_song()
            if prev:
                self._play_song(prev)
            else:
                QMessageBox.information(self, "Info", "There is no previous song.")
            return

        # HOME mode: VIBE first
        if self.playlist.current:
            current_song = self.playlist.current.data
            vibe_prev = self.controller.get_prev_same_vibe(current_song)

            if vibe_prev:
                self._play_song(vibe_prev)
                return

        # fallback dll
        prev = self.playlist.prev_song()
        if prev:
            self._play_song(prev)
        else:
            QMessageBox.information(self, "Info", "There is no previous song.")

    # REFRESH DARI ADMIN
    def refresh_songs_from_controller(self):
        all_songs = self.controller.get_all_songs()

        self.playlist.clear()
        for s in all_songs:
            self.playlist.add_last(s)

        for name, dll in list(self.playlists.items()):
            new_dll = DoubleLinkedList()
            for song in dll.to_list():
                if self.controller.find_song(song.judul, song.artis):
                    new_dll.add_last(song)
            self.playlists[name] = new_dll

        new_fav = set()
        for (j, a) in self.favorites:
            if self.controller.find_song(j, a):
                new_fav.add((j, a))
        self.favorites = new_fav

        new_q = Queue()
        while not self.queue.is_empty():
            s = self.queue.dequeue()
            if self.controller.find_song(s.judul, s.artis):
                new_q.enqueue(s)
        self.queue = new_q

        if self.playlist.current:
            cur_song = self.playlist.current.data
            if not self.controller.find_song(cur_song.judul, cur_song.artis):
                self.playlist.current = None
                self.lbl_now.setText("No song is playing")

        self.refresh_current_view()

    def refresh_current_view(self):
        if self.current_view_name == "playlists":
            self._show_playlist_view()
        elif self.current_view_name == "all_songs":
            self._show_all_songs()
        elif self.current_view_name == "playlist_detail":
            if self.viewing_playlist_name and self.viewing_playlist_name in self.playlists:
                dll = self.playlists[self.viewing_playlist_name]
                self._show_playlist_detail(self.viewing_playlist_name, dll)
            else:
                self._show_all_songs()
        elif self.current_view_name == "favorites":
            self._show_favorites_view()
        elif self.current_view_name == "history":
            self._show_history_view()
        elif self.current_view_name == "queue":
            self._show_queue_view()
        elif self.current_view_name == "search":
            self._show_search_results(self.search.text())

    # BACK BUTTON
    def _back_from_detail(self):
        if self.current_view_name in ("playlist_detail", "favorites", "history", "queue"):
            self._show_playlist_view()
        else:
            self._show_all_songs()

    # LOGOUT
    def _action_logout(self):
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

    from gui.login_window import LoginWindow
    login = LoginWindow()
    w = UserWindow(login_window_ref=login)
    w.show()
    sys.exit(app.exec())