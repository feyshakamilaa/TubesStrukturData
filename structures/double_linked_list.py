# structures/double_linked_list.py
from structures.node import Node
from structures.song import Song


class DoubleLinkedList:
    """
    Double Linked List khusus untuk pemutar musik.
    Kompatibel dengan UserWindow GUI baru.
    """

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.current: Node | None = None
        self.size = 0

    # INSERT
    def add_last(self, song: Song):
        new_node = Node(song)

        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1

    def add_first(self, song: Song):
        new_node = Node(song)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    # DELETE (optional, playlist)
    def delete_at(self, index: int):
        if index < 0 or index >= self.size:
            return False

        if self.size == 1:
            self.clear()
            return True

        # delete head
        if index == 0:
            if self.current == self.head:
                self.current = self.head.next
            self.head = self.head.next
            self.head.prev = None
            self.size -= 1
            return True

        # delete tail
        if index == self.size - 1:
            if self.current == self.tail:
                self.current = self.tail.prev
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1
            return True

        # delete middle
        node = self.get_node(index)
        if self.current == node:
            self.current = node.next or node.prev

        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return True

    def get_node(self, index: int):
        if index < 0 or index >= self.size:
            return None
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

    # PLAYBACK (DISIMPLEKAN)
    def play_first(self):
        """Set current ke head dan return lagunya."""
        if not self.head:
            return None
        self.current = self.head
        return self.current.data

    def next_song(self):
        """Circular next song (normal playlist navigation)."""
        if not self.current:
            return None

        # normal next
        if self.current.next:
            self.current = self.current.next
            return self.current.data

        # circular, kembali ke head
        self.current = self.head
        return self.current.data

    def prev_song(self):
        """Circular previous song (normal playlist navigation)."""
        if not self.current:
            return None

        # normal prev
        if self.current.prev:
            self.current = self.current.prev
            return self.current.data

        # circular, kembali ke tail
        self.current = self.tail
        return self.current.data

    def jump_to_song(self, song: Song):
        """Loncat ke node yang lagunya sama."""
        cur = self.head
        while cur:
            if cur.data.judul == song.judul and cur.data.artis == song.artis:
                self.current = cur
                return cur
            cur = cur.next
        return None

    # HELPERS
    def to_list(self):
        """Konversi list untuk UI playlist & favorites."""
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.data)
            cur = cur.next
        return arr

    def clear(self):
        """Reset seluruh list."""
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0
        
    def remove(self, target):
        current = self.head
        while current:
            if current.data == target:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self.size -= 1
                return True

            current = current.next

        return False