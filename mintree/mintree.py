from typing import TypeVar, Generic
import unittest

T = TypeVar("T")


class MinHeap(Generic[T]):
    def __init__(self):
        self._items = []

    def extract_root(self):
        if len(self._items) == 0:
            return None

        val = self._items[0]
        self._items[0] = self._items[len(self._items) - 1]
        self._items.pop()
        self.heapify(0)
        return val

    def left_index(self, index: int):
        return index * 2 + 1

    def right_index(self, index: int):
        return index * 2 + 2

    def parent_index(self, index: int):
        return (index - 1) // 2

    # Start from root and traverse down to correct any incorrect subtrees
    def heapify(self, index: int):
        # Find the smaller of index, left or right
        l_index = self.left_index(index)
        r_index = self.right_index(index)
        smallest = index
        if l_index < len(self._items) and self._items[l_index] < self._items[smallest]:
            smallest = l_index
        if r_index < len(self._items) and self._items[r_index] < self._items[smallest]:
            smallest = r_index
        if smallest != index:
            tmp = self._items[index]
            self._items[index] = self._items[smallest]
            self._items[smallest] = tmp
            self.heapify(smallest)

    def add(self, new_item: T):
        self._items.append(new_item)
        index = len(self._items) - 1

        while index > 0 and self._items[self.parent_index(index)] > new_item:
            self._items[index] = self._items[self.parent_index(index)]
            index = self.parent_index(index)
        self._items[index] = new_item


def min_heap_extractor(heap: MinHeap[T]) -> T:
    next_val = heap.extract_root()
    while next_val is not None:
        yield next_val
        next_val = heap.extract_root()


class TestMinTree(unittest.TestCase):
    def testHappyPath(self):
        heap = MinHeap[int]()
        for i in [5, 2, 7, 5, 9, 3, 5, 1, 6]:
            heap.add(i)

        back = []
        for i in min_heap_extractor(heap):
            back.append(i)

        self.assertEqual(back, [1, 2, 3, 5, 5, 5, 6, 7, 9])
        print(f"Back: {back}")


if __name__ == "__main__":
    unittest.main()
