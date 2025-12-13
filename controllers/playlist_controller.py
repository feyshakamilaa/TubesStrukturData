# controllers/playlist_controller.py
from structures.playlist import Playlist

class PlaylistController:
    def __init__(self):
        self.playlists = []

    def create_playlist(self, name, cover_path=None):
        playlist = Playlist(name, cover_path)
        self.playlists.append(playlist)
        return playlist

    def get_all_playlists(self):
        return self.playlists

    def find_by_id(self, playlist_id):
        for p in self.playlists:
            if p.id == playlist_id:
                return p
        return None