import unittest


class Node:
    def __init__(self, next_, data):
        self.next = next_
        self.data = data


def kth_from_last_recurse(node, k) -> tuple[int, Node]:
    """
    Return the index from end of node and the kth node from the end (or None if it's not yet found)
    """
    if node is None:
        return -1, None

    next_from_last, ret_node = kth_from_last_recurse(node.next, k)
    this_from_last = next_from_last + 1
    if k == this_from_last:
        assert not ret_node
        ret_node = node

    return this_from_last, ret_node


def get_kth_from_last(node: Node, k: int) -> Node:
    inx, ret_node = kth_from_last_recurse(node, k)
    return ret_node


class TestKthFromLast(unittest.TestCase):
    def test_happy_path(self):
        node = None
        for i in range(0, 5):
            node = Node(node, i)

        self.assertEqual(get_kth_from_last(node, 3).data, 3)


if __name__ == "__main__":
    unittest.main()