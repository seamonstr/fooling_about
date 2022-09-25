import unittest

LAST_PRINTABLE = ord('~')
FIRST_PRINTABLE = ord(' ')


def inx_for_char(c: str) -> int:
    assert FIRST_PRINTABLE <= ord(c) <= LAST_PRINTABLE
    return ord(c) - FIRST_PRINTABLE


def is_permutation_palindrome(in_str: str) -> bool:
    char_counts = (LAST_PRINTABLE - FIRST_PRINTABLE) * [0]
    in_str = in_str.lower()
    for c in in_str:
        if c not in ' \t\n\r':
            char_counts[inx_for_char(c)] += 1
    found_odd = False
    for i in char_counts:
        if i % 2 == 1:
            if found_odd:
                return False
            else:
                found_odd = True
    return True


class TestPermutationPalindrome (unittest.TestCase):
    test_data = [
        ("abcdedcba", True),
        ("blahblah", True),
        ("BLAHblah", True),
        ("b  lah blah", True),
        ("    blahblah   ", True),
        ("", True),
        ("iiiiiiiiii", True),
        ("i", True),
        ("nope", False),
    ]
    
    def test_cases(self):
        for in_str, result in TestPermutationPalindrome.test_data:
            with self.subTest(test_str = in_str):
                self.assertEqual(is_permutation_palindrome(in_str), result)
            
            
if __name__ == '__main__':
    unittest.main()
