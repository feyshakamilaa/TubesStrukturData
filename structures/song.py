# structures/song.py
import uuid

class Song:
    def __init__(self, judul, artis, genre, vibes, file_path=None, cover_path=None):
        self.id = str(uuid.uuid4())
        self.judul = judul
        self.artis = artis
        self.genre = genre
        self.vibes = vibes
        self.file_path = file_path
        self.cover_path = cover_path

    def to_dict(self):
        return {
            "judul": self.judul,
            "artis": self.artis,
            "genre": self.genre,
            "vibes": self.vibes,
            "file_path": self.file_path,   
        }

    def __str__(self):
        return f"{self.judul} - {self.artis} ({self.genre}, {self.vibes})"
    
    def __eq__(self, other):
        return isinstance(other, Song) and self.id == other.id