# controllers/lagu_controller.py

import os
from structures.double_linked_list import DoubleLinkedList
from structures.song import Song
from structures.single_linked_list import SingleLinkedList
from structures.multi_linked_list import MultiLinkedList

class SongController:
    """
    Controller lagu dengan:
    - DoubleLinkedList (data utama)
    - MultiLinkedList (index vibes)
    """

    def __init__(self):
        self.songs = DoubleLinkedList()
        self.vibe_index = MultiLinkedList()

        self._load_default_songs()
        self.rebuild_vibe_index()

    # LOAD DEFAULT SONGS 
    def _load_default_songs(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        music_dir = os.path.join(BASE_DIR, "assets", "music")
        cover_dir = os.path.join(BASE_DIR, "assets", "cover")

        default_songs = [
            ("Belum Ada Satu Bulan", "Bernadya", "Pop", "Sad",
            "Belum Ada Satu Bulan - Bernadya - Pop - Sad"),
            
            ("Best Part", "Daniel Caesar & H.E.R", "R&B", "Chill",
            "Best Part - Daniel Caesar & H.E.R - R&B - Chill"),

            ("Dunia Tipu-Tipu", "Yura Yunita", "Pop", "Chill",
            "Dunia Tipu-Tipu - Yura Yunita - Pop - Chill"),

            ("Easy On Me", "Adele", "Ballad", "Emotional",
            "Easy On Me - Adele - Ballad - Emotional"),

            ("Electric Love", "BØRNS", "Indie Pop", "Energetic",
            "Electric Love - BØRNS - Indie Pop - Energetic"),

            ("Feeling Good", "Michael Bublé", "Jazz", "Powerful",
            "Feeling Good - Michael Bublé - Jazz - Powerful"),

            ("Fly Me to the Moon", "Frank Sinatra", "Jazz", "Chill",
            "Fly Me to the Moon - Frank Sinatra - Jazz - Chill"),

            ("Glimpse of Us", "Joji", "Ballad", "Emotional",
            "Glimpse of Us - Joji - Ballad - Emotional"),

            ("God's Plan", "Drake", "Hip-Hop", "Chill",
            "God_s - Plan - Drake - Hip-Hop - Chill"),

            ("Hati-Hati di Jalan", "Tulus", "Pop", "Sad",
            "Hati-Hati di Jalan - Tulus - Pop - Sad"),

            ("Kill This Love", "BLACKPINK", "K-Pop", "Energetic",
            "Kill This Love - BLACKPINK - K-Pop - Energetic"),

            ("Levitating", "Dua Lipa", "Pop", "Happy",
            "Levitating - Dua Lipa - Pop - Happy"),

            ("Love on the Brain", "Rihanna", "R&B", "Emotional",
            "Love on the Brain - Rihanna - R&B - Emotional"),

            ("Love Scenario", "iKON", "K-Pop", "Chill",
            "Love Scenario - iKON - K-Pop - Chill"),

            ("Rasa Ini", "Vierra", "Pop", "Sad",
            "Rasa Ini - Vierra - Pop - Sad"),

            ("Riptide", "Vance Joy", "Indie Folk", "Happy",
            "Riptide - Vance Joy - Indie Folk - Happy"),

            ("Shape of You", "Ed Sheeran", "Pop", "Happy",
            "Shape of You - Ed Sheeran - Pop - Happy"),

            ("Sicko Mode", "Travis Scott", "Hip-Hop", "Energetic",
            "Sicko Mode - Travis Scott - Hip-Hop - Energetic"),

            ("Sorai", "Nadin Amizah", "Pop", "Chill",
            "Sorai - Nadin Amizah - Pop - Chill"),

            ("The Kill", "Thirty Seconds to Mars", "Rock", "Intense",
            "The Kill - Thirty Seconds to Mars - Rock - Intense"),

            ("The Night We Met", "Lord Huron", "Indie", "Sad",
            "The Night We Met - Lord Huron - Indie - Sad"),

            ("Garam dan Madu (Sakit Dadaku)", "Tenxi", "Pop", "Galau",
            "Garam dan Madu (Sakit Dadaku) - Tenxi - Pop - Galau"),

            ("Alamak", "Rizky Febian", "Pop", "Fun",
            "Alamak - Rizky Febian - Pop - Fun"),

            ("Tabola Bale", "Silet Open Up", "Lagu Daerah NTT", "Upbeat",
            "Tabola Bale - Silet Open Up - Lagu Daerah NTT - Upbeat"),

            ("Lesung Pipi", "Raim Laode", "Pop", "Sweet",
            "Lesung Pipi - Raim Laode - Pop - Sweet"),

            ("Stecu Stecu", "Faris Adam", "Pop", "Upbeat",
            "Stecu Stecu - Faris Adam - Pop - Upbeat"),
        ]


        for judul, artis, genre, vibes, filename in default_songs:
            self.songs.add_last(
                Song(
                    judul,
                    artis,
                    genre,
                    vibes,
                    os.path.join(music_dir, f"{filename}.mp3"),
                    os.path.join(cover_dir, f"{filename}.jpg"),
                )
            )

    # GET DATA
    def get_all_songs(self):
        return self.songs.to_list()

    def find_song_by_id(self, song_id):
        node = self.songs.head
        while node:
            if node.data.id == song_id:
                return node.data
            node = node.next
        return None

    # SEARCH
    def search(self, keyword):
        if not keyword:
            return self.get_all_songs()

        keyword = keyword.lower().strip()
        sll = SingleLinkedList()

        node = self.songs.head
        while node:
            sll.add_last(node.data)
            node = node.next

        return sll.search(keyword)

    # CRUD (ADMIN)
    def add_song(self, song: Song):
        self.songs.add_last(song)
        self.vibe_index.add_song_to_vibe(song)

    def update_song(self, song_id, judul, artis, genre, vibes, file_path=None, cover_path=None):
        node = self.songs.head
        while node:
            if node.data.id == song_id:
                node.data.judul = judul
                node.data.artis = artis
                node.data.genre = genre
                node.data.vibes = vibes
                if file_path:
                    node.data.file_path = file_path
                if cover_path:
                    node.data.cover_path = cover_path
                self.rebuild_vibe_index()
                return True
            node = node.next
        return False

    def delete_song_by_id(self, song_id):
        idx = 0
        node = self.songs.head
        while node:
            if node.data.id == song_id:
                self.songs.delete_at(idx)
                self.rebuild_vibe_index()
                return True
            node = node.next
            idx += 1
        return False

    # VIBE NAVIGATION (MULTI LINKED LIST)
    def rebuild_vibe_index(self):
        self.vibe_index.rebuild(self.get_all_songs())

    def get_songs_by_vibe(self, vibe_name):
        return self.vibe_index.get_songs_by_vibe(vibe_name)

    def get_next_same_vibe(self, current_song):
        return self.vibe_index.get_next_song_same_vibe(current_song)

    def get_prev_same_vibe(self, current_song):
        return self.vibe_index.get_prev_song_same_vibe(current_song)