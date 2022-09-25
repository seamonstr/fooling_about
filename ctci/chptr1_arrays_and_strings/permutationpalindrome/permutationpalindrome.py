import unittest

CASE_DIFFERENCE = ord('a') - ord('A')


def inx_for_char(c: str) -> int:
    char_code = ord(c)
    # If it's above the upper case region, it might be lower case - bring it into the upper case range
    if char_code > ord('Z'):
        char_code -= CASE_DIFFERENCE
    assert ord('A') <= char_code <= ord('Z')

    # Return an index into a list where 'A' is 0
    char_code -= ord('A')
    return char_code


def is_permutation_palindrome(in_str: str) -> bool:
    char_counts = (ord('Z') - ord('A')) * [0]
    for c in in_str:
        if c not in ' \t\n\r':  # Ignore all whitespace
            char_counts[inx_for_char(c)] += 1
    found_odd = False
    for i in char_counts:
        if i % 2 == 1:
            if found_odd:
                return False
            else:
                found_odd = True
    return True


def toggle_bit(flags: int, bit: int) -> int:
    return flags ^ (1 << bit)


def bitwise_is_permutation_palindrome(in_str: str) -> bool:
    char_flags = int()
    for c in in_str:
        if c == ' ':
            continue
        char_flags = toggle_bit(char_flags, inx_for_char(c))

    return char_flags & (char_flags - 1) == 0


class TestPermutationPalindrome (unittest.TestCase):
    test_data = [
        ("abcdedcba", True),
        ("blahblah", True),
        ("BLAHblah", True),
        ("abcabcde", False),
        ("b  lah blah", True),
        ("    blahblah   ", True),
        ("", True),
        ("iiiiiiiiii", True),
        ("i", True),
        ("nope", False),
    ]
    
    def run_test_cases(self, function):
        for in_str, result in TestPermutationPalindrome.test_data:
            with self.subTest(test_str = in_str):
                self.assertEqual(function(in_str), result)

    def test_list_solution(self):
        self.run_test_cases(is_permutation_palindrome)

    def test_bitvector_solution(self):
        self.run_test_cases(bitwise_is_permutation_palindrome)


if __name__ == '__main__':
    unittest.main()
