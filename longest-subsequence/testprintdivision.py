import unittest
from getdecimal import get_decimal


class TestPrintDivision(unittest.TestCase):
    def test_get_decimal(self):
        test_data = [(1, 2, "0.5"), (1, 1, "1"), (1, 3, "0.(3)"), (400, 11, "36.(36)")]

        for (numerator, denominator, result) in test_data:
            self.assertEqual(result, get_decimal(numerator, denominator))


if __name__ == "__main__":
    unittest.main()
