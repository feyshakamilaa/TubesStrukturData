# controllers/shared.py

from controllers.lagu_controller import SongController

# controller global dibuat sekali
_shared_song_controller = SongController()

def get_song_controller():
    return _shared_song_controller