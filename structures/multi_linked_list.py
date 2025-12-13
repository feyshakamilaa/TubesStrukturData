# structures/multi_linked_list.py

class VibeNode:
    """Node penyimpanan lagu dengan pointer untuk navigasi vibe."""
    def __init__(self, song):
        self.song = song
        self.mood_up = None
        self.mood_down = None
        self.energy_up = None
        self.energy_down = None


class MultiLinkedList:
    """
    Multi Linked List untuk navigasi berdasarkan vibes.
    Key: (judul.lower(), artis.lower())
    """
    def __init__(self):
        self.nodes = {}

    # ----------------------------
    # Helper
    # ----------------------------
    def _key(self, song):
        return (song.judul.lower(), song.artis.lower())

    def add_song(self, song):
        key = self._key(song)
        if key not in self.nodes:
            self.nodes[key] = VibeNode(song)

    def add_song_to_vibe(self, song):
        self.add_song(song)

    # VIBE SCORE MAPPING (OPSI A)
    def _vibe_score(self, song):
        """Mapping vibes → (mood, energy) score."""
        vibe = (song.vibes or "").lower()
        if vibe == "happy":
            return (3, 3)
        if vibe == "chill":
            return (2, 1)
        if vibe == "sad":
            return (1, 1)

        # vibes tidak dikenal
        return (0, 0)

    # AUTO-CONNECT
    def rebuild(self, songs):
        """Bangun ulang MLL berdasarkan daftar lagu dari DLL."""
        self.nodes = {}

        # 1. Tambah node untuk semua lagu
        for s in songs:
            self.add_song(s)

        # 2. Kelompokkan lagu berdasarkan vibes
        buckets = {}
        for s in songs:
            buckets.setdefault(s.vibes, []).append(s)

        # 3. Untuk setiap vibe, urutkan dengan hubungkan node
        for vibe, arr in buckets.items():

            # urutkan berdasarkan skor vibe
            arr_sorted = sorted(arr, key=lambda x: self._vibe_score(x))

            # hubungkan node
            for i in range(len(arr_sorted)):
                cur = arr_sorted[i]
                cur_node = self.nodes[self._key(cur)]

                # mood_up / mood_down
                if i + 1 < len(arr_sorted):
                    nxt = arr_sorted[i + 1]
                    cur_node.mood_up = self.nodes[self._key(nxt)]

                if i - 1 >= 0:
                    prev = arr_sorted[i - 1]
                    cur_node.mood_down = self.nodes[self._key(prev)]

                # energy_up/down = mirror mood
                cur_node.energy_up = cur_node.mood_up
                cur_node.energy_down = cur_node.mood_down

    # NEXT / PREV VIBE NAVIGATION
    def get_next_vibe(self, song):
        node = self.nodes.get(self._key(song))
        if not node:
            return None

        # Prioritas next vibe
        if node.mood_up:
            return node.mood_up.song
        if node.energy_up:
            return node.energy_up.song
        if node.mood_down:
            return node.mood_down.song
        if node.energy_down:
            return node.energy_down.song

        return None

    def get_prev_vibe(self, song):
        node = self.nodes.get(self._key(song))
        if not node:
            return None

        if node.mood_down:
            return node.mood_down.song
        if node.energy_down:
            return node.energy_down.song
        if node.mood_up:
            return node.mood_up.song
        if node.energy_up:
            return node.energy_up.song

        return None

    # Alias untuk kompatibilitas user_window.py
    def get_next_song_same_vibe(self, song):
        return self.get_next_vibe(song)

    def get_prev_song_same_vibe(self, song):
        return self.get_prev_vibe(song)