# structures/playlist.py
import uuid
from structures.double_linked_list import DoubleLinkedList

class Playlist:
    def __init__(self, name, cover_path=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.cover_path = cover_path
        self.songs = DoubleLinkedList()

    def add_song(self, song):
        self.songs.add_last(song)

    def add_songs(self, songs):
        for song in songs:
            self.add_song(song)

    def remove_song(self, song_id):
        idx = 0
        node = self.songs.head
        while node:
            if node.data.id == song_id:
                self.songs.delete_at(idx)
                return True
            node = node.next
            idx += 1
        return False

    def get_all_songs(self):
        return self.songs.to_list()