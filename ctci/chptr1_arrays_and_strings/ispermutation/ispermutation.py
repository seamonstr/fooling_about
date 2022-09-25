import unittest


def str_to_dict(str_: str) -> dict:
    return_val = {}
    for c in str_:
        if c in return_val:
            return_val[c] += 1
        else:
            return_val[c] = 0
    return return_val


# O(n)
def is_permutation(source: str, permutation: str) -> bool:
    return str_to_dict(source) == str_to_dict(permutation)


FIRST_PRINTABLE_ASCII = 32  # Space
LAST_PRINTABLE_ASCII = 126  # Tilde


# Also O(n), but more efficient - no dict to allocate, no hashing, ...
def is_permutation_no_dict(source: str, permutation: str) -> bool:
    counts = [0] * LAST_PRINTABLE_ASCII - FIRST_PRINTABLE_ASCII
    for c in source:
        counts[ord(c) - FIRST_PRINTABLE_ASCII] += 1

    for c in permutation:
        counts[ord(c) - FIRST_PRINTABLE_ASCII] -= 1
        if counts[ord(c) - FIRST_PRINTABLE_ASCII] < 0:
            return False

    for i in counts:
        if counts[i] != 0:
            return False
    return True


class TestIsPermutation(unittest.TestCase):
    test_data = [
        ("thisisthesource", "sourceisthethis", True),
        ("mmmmmultiplecharacterscount", "multiplemcharactersmcountmm", True),
        ("", "", True),
        ("thisoneisn't", "nope,deffo not", False),
        ("justonedifferencea", "justonedifference", False),
        ("adifferencejustone", "differencejustone", False),
        ("", "nope", False),
        ("nuh-uh", "", False),
        ("indifferenttocase", "IndifferentToCase", False),
    ]

    def run_test(self, func):
        for source, permutation, result in TestIsPermutation.test_data:
            self.assertEquals(result, is_permutation(source, permutation))

    def testWithDict(self):
        self.run_test(is_permutation)

    def testNoDict(self):
        self.run_test(is_permutation_no_dict)


if __name__ == "__main__":
    unittest.main()
