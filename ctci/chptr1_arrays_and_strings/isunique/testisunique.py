import unittest
from .isunique import is_unique_n, is_unique_n_squared


class TestIsUnique(unittest.TestCase):
    test_data = [
        ("abcdefghijklmnopqrstuvwxyz", True),
        ("abcdefgajklmnop", False),
        ("", True),
        ("abcdefga", False),
        ("aa", False),
        ("Aa", True),
    ]

    def testHappyPath(self, func=is_unique_n):
        for string, result in TestIsUnique.test_data:
            self.assertEqual(func(string), result)

    def testEfficientHappyPath(self):
        self.testHappyPath(is_unique_n_squared)


if __name__ == "__main__":
    unittest.main()
