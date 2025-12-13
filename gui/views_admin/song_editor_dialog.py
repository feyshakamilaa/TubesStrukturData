# gui/views_admin/song_editor_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QFont

class SongEditorDialog(QDialog):
    def __init__(self, parent, mode="add", song=None):
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Music")

        # PERBESAR POPUP
        self.setFixedSize(480, 420)
        self.file_path = None
        self.cover_path = None

        # ROOT LAYOUT
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # FORM LAYOUT
        form = QFormLayout()
        form.setSpacing(18)  # spacing antar field

        # INPUT 
        def styled_input(placeholder):
            box = QLineEdit()
            box.setPlaceholderText(placeholder)
            box.setFixedHeight(48)
            box.setFont(QFont("Arial", 12))
            box.setStyleSheet("""
                QLineEdit {
                    background-color: #1b1b1b;
                    border: 2px solid #00ff87;
                    border-radius: 10px;
                    padding-left: 12px;
                    font-size: 15px;
                    color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #40ff9b;
                    background-color: #222;
                }
            """)
            return box

        # INPUT FIELDS
        self.inp_judul = styled_input("Song Title")
        self.inp_artis = styled_input("Artist")
        self.inp_genre = styled_input("Genre")
        self.inp_vibes = styled_input("Vibes (e.g., chill, upbeat, mellow)")

        # Jika mode edit maka isi field
        if mode == "edit" and song:
            self.inp_judul.setText(song.judul)
            self.inp_artis.setText(song.artis)
            self.inp_genre.setText(song.genre)
            self.inp_vibes.setText(song.vibes)
            self.file_path = song.file_path
            self.cover_path = song.cover_path

        # Tambahkan ke form
        form.addRow("Title:", self.inp_judul)
        form.addRow("Artist:", self.inp_artis)
        form.addRow("Genre:", self.inp_genre)
        form.addRow("Vibes:", self.inp_vibes)

        layout.addLayout(form)
        
    # FILE MUSIK
        self.btn_file = QPushButton("Choose Music File (.mp3)")
        self.btn_file.setFixedHeight(40)
        self.btn_file.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        self.btn_file.clicked.connect(self._choose_file)
        layout.addWidget(self.btn_file)

        # COVER IMAGE
        self.btn_cover = QPushButton("Choose Cover Image (jpg/png)")
        self.btn_cover.setFixedHeight(40)
        self.btn_cover.clicked.connect(self._choose_cover)
        layout.addWidget(self.btn_cover)

        # TOMBOL SIMPAN / TAMBAH
        btn_text = "Add" if mode == "add" else "Save"

        self.save_btn = QPushButton(btn_text)
        self.save_btn.setFixedHeight(48)
        self.save_btn.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff87;
                color: black;
                border-radius: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #40ff9b;
            }
        """)

        self.save_btn.clicked.connect(self._save)
        layout.addWidget(self.save_btn)

        self.saved_data = None
        self.mode = mode

    def _choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File Musik",
            "",
            "Audio Files (*.mp3 *.wav)"
        )
        if path:
            self.file_path = path
            self.btn_file.setText("✔ File Musik Dipilih")

    def _choose_cover(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih Cover Lagu",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if path:
            self.cover_path = path
            self.btn_cover.setText("✔ Cover Dipilih")

    # HANDLE SAVE DATA
    def _save(self):
        judul = self.inp_judul.text().strip()
        artis = self.inp_artis.text().strip()
        genre = self.inp_genre.text().strip()
        vibes = self.inp_vibes.text().strip()

        if not all([judul, artis, genre, vibes]):
            QMessageBox.warning(self, "Error", "Semua kolom wajib diisi!")
            return

        if not self.file_path:
            QMessageBox.warning(self, "Error", "File musik wajib dipilih!")
            return

        self.saved_data = (
            judul,
            artis,
            genre,
            vibes,
            self.file_path,
            self.cover_path
        )
        self.accept()

    def get_data(self):
        return self.saved_data