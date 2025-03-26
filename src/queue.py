class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)

    def is_empty(self):
        """Return True if the queue is empty, False otherwise."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def peek(self):
        """Return the item at the front of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue")
        return self._items[0]
