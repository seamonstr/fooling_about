from unittest import TestCase

from foldlist import LinkedList


def test_equal_to(test, ll, values):
    node = ll.root
    for value in values:
        test.assertIsNotNone(node, "Ran out of values too early")
        test.assertEqual(value, node.val, "Values don't match source")
        node = node.next_

    test.assertIsNone(node, "values remaining in the linked list")


class TestListCreation(TestCase):
    def test_create_list(self):
        happy_cases = [
            [1],
            [1, 2, 3, 4],
            []
        ]

        for i in happy_cases:
            with self.subTest(f"create list with {i}", i=i):
                self.test_equal_to(LinkedList(i), i)

    def test_get_node_by_index(self):
        ll = LinkedList([1, 2, 3, 4, 5])
        self.assertIsNone(ll.node_by_index(0))
        self.assertEqual(1, ll.node_by_index(1).val)
        self.assertEqual(5, ll.node_by_index(5).val)
        self.assertIsNone(ll.node_by_index(10))

    def test_move_node(self):
        happy_cases = [
            ([1, 2], 1, 2, [2, 1]),
            ([1, 2, 3, 4, 5, 6], 1, 6, [6, 2, 3, 4, 5, 1]),
            ([1, 2, 3, 4, 5, 6], 3, 4, [1, 2, 4, 3, 5, 1]),
        ]

        for (values, from_, to, expected) in happy_cases:
            with self.subTest(f"move {from_} to {to} within {values}"):
                ll = LinkedList(values)
                ll.move_node(ll.node_by_index(from_), ll.node_by_index(to))
                test_equal_to(self, ll, expected)


class TestFoldList(TestCase):
    def test_happycase(self):
        happycases = [
            ([1, 2, 3, 4, 5, 6, 7, 8], [1, 8, 2, 7, 3, 6, 4, 5]),
            ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
            ([1], [1]),
            ([], [])
        ]

        for (test, expected) in happycases:
            with self.subTest(f"Fold test with {test}"):
                ll = LinkedList(test)
                ll.fold()
                print(ll)
                test_equal_to(self, ll, expected)
