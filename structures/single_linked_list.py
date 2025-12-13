from structures.song import Song

class SLLNode:
    def __init__(self, data: Song):
        self.data = data
        self.next = None


class SingleLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # -------------------------
    # INSERT
    # -------------------------
    def add_last(self, data: Song):
        new_node = SLLNode(data)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.size += 1

    # -------------------------
    # SEARCH berdasarkan keyword
    # -------------------------
    def search(self, keyword: str):
        keyword = keyword.lower().strip()
        result = []

        cur = self.head
        while cur:
            s = cur.data
            if (keyword in s.judul.lower() or
                keyword in s.artis.lower() or
                keyword in s.genre.lower() or
                keyword in s.vibes.lower()):
                result.append(s)
            cur = cur.next

        return result

    # -------------------------
    # TRAVERSE
    # -------------------------
    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result
