# structures/stack.py

class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def is_empty(self):
        return self.top is None

    def push(self, item):
        """Tambah data ke atas stack"""
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        """Ambil data dari atas stack"""
        if self.is_empty():
            return None

        removed = self.top
        self.top = removed.next
        self._size -= 1
        return removed.data

    def peek(self):
        return None if self.is_empty() else self.top.data

    def size(self):
        return self._size

    def display(self):
        """Return isi stack dari atas ke bawah"""
        result = []
        cur = self.top
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result