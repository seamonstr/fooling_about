import pytest
# Implement slow/fast pointer search through a linked list to find
# the middle item in the list.


class Node:
    def __init__(self, value):
        self.next = None
        self.value = value


def ll_from_list(list_):
    root = Node(list_[0])
    prev = root

    for i in list_[1:]:
        new_node = Node(i)
        prev.next = new_node
        prev = new_node

    return root


def middle_node(root: Node) -> Node:
    # Slow/fast
    slow = root
    fast = root

    # Run forward until fast bumps the end; slow should be on
    # the middle.  Or should it...?
    while fast.next and fast.next.next:
        fast = fast.next.next
        slow = slow.next

    # slow will always be at fast // 2.  For lists with
    # an even number, that's right.
    # For an odd number (ie. fast still has one more node to go),
    # slow will still be at  fast // 2 (ie. if there's 11, it'll be at
    # 5). So we want slow.next!
    if fast.next:
        return slow.next
    else:
        return slow


def test_happy_path():
    root = ll_from_list([i for i in range(1, 10)])
    assert middle_node(root).value == 5

    root = ll_from_list([i for i in range(1, 11)])
    assert middle_node(root).value == 6
