import unittest
from .urlify import urlify


class TestUrlify(unittest.TestCase):
    test_data = [
        ("some stuff with spaces      ", 22, "some%20stuff%20with%20spaces"),
        ("nospaces", 8, "nospaces"),
        ("", 0, ""),
        ("spaceatend   ", 11, "spaceatend%20"),
        (" spaceatstart  ", 13, "%20spaceatstart"),
    ]

    def test_with_testdata(self):
        for test, length, result in TestUrlify.test_data:
            self.assertEqual(urlify(test, length), result)


if __name__ == "__main__":
    unittest.main()
