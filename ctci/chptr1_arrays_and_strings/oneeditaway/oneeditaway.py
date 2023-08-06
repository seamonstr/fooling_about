import unittest


def check_for_edit(string_a, string_b):
    change_found = False
    a_inx = b_inx = 0
    while b_inx < len(string_b) and a_inx < len(string_a):
        if string_a[a_inx] != string_b[b_inx]:
            if change_found:
                return False
            change_found = True
            b_inx += 1
            if len(string_a) == len(string_b):
                a_inx += 1
        else:
            a_inx += 1
            b_inx += 1

    return True


def is_one_edit_away(string_a: str, string_b: str) -> bool:
    if abs(len(string_a) - len(string_b)) > 1:
        return False

    if len(string_a) >= len(string_b):
        return check_for_edit(string_b, string_a)
    else:
        return check_for_edit(string_a, string_b)


class TestOneEditAway(unittest.TestCase):
    test_data = [
        ("abcd", "abbcd", True),
        ("abcd", "acd", True),
        ("abcd", "aacd", True),
        ("abcd", "abce", True),
        ("abcd", "abcde", True),
        ("abcd", "abc", True),
        ("abccc", "abddc", False),
        ("deffo", "not", False),
    ]

    def test_with_test_data(self):
        for string_a, string_b, result in TestOneEditAway.test_data:
            with self.subTest(f"{string_a} and {string_b}"):
                self.assertEqual(is_one_edit_away(string_a, string_b), result)


if __name__ == "__main__":
    unittest.main()
