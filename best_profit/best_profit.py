import unittest


def best_profit(data: list[int]) -> int:
    if len(data) == 0:
        return 0

    best = 0
    lowest_element = data[0]

    for i in data[1 : len(data)]:
        lowest_element = min(lowest_element, i)
        best = max(best, i - lowest_element)

    return best


class BestProfitTest(unittest.TestCase):
    test_data = [
        [[7, 1, 5, 3, 6, 4], 5],
        [[0, 5, 3, 6, -1, 8, -2, 10, 0], 12],
        [[], 0],
        [[1], 0],
        [[1, 2], 1],
    ]

    def test_happy_path(self):
        for t in BestProfitTest.test_data:
            self.assertEqual(best_profit(t[0]), t[1])


if __name__ == "__main__":
    unittest.main()
