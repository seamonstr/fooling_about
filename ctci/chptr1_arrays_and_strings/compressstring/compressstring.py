import unittest
from io import StringIO


def write_char(char: str, count: int, destination: StringIO) -> int:
    return destination.write(f"{count}{char}")


def compress_string(input_string: str) -> str:
    if len(input_string) <= 2:
        return input_string

    compressed = StringIO()
    current_char = input_string[0]
    current_count = 1
    written = 0
    for c in input_string[1:]:
        if c != current_char:
            written += write_char(current_char, current_count, compressed)
            current_char = c
            current_count = 0
        current_count += 1

    if current_count > 0:
        written += write_char(current_char, current_count, compressed)

    if len(input_string) <= written:
        return input_string
    else:
        return compressed.getvalue()


class TestCompressString(unittest.TestCase):
    test_data = [
        ("aabcccdddaaab", "2a1b3c3d3a1b"),
        ("nobenefit", "nobenefit"),
        ("aabbccdd", "aabbccdd"),
        ("", ""),
        ("aa", "aa"),
        ("ab", "ab"),
        ("aaaaaaaa", "8a")
    ]

    def test_compress_string(self):
        for test_string, expected in TestCompressString.test_data:
            with self.subTest(test_string):
                self.assertEqual(compress_string(test_string), expected)


if __name__ == "__main__":
    unittest.main()