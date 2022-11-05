import copy
import unittest


def nullify_row(i, return_matrix):
    return_matrix[i] = [0] * len(return_matrix[0])


def nullify_cols(i, return_matrix):
    for row in return_matrix:
        row[i] = 0


def zero_matrix(matrix):
    size_x = len(matrix[0])
    size_y = len(matrix)
    zero_rows = size_y * [0]
    zero_cols = size_x * [0]

    for row_index, row in enumerate(matrix):
        for col_index, col in enumerate(row):
            if col == 0:
                zero_cols[col_index] = 1
                zero_rows[row_index] = 1

    return_matrix = copy.deepcopy(matrix)

    for i, is_zero in enumerate(zero_rows):
        if is_zero:
            nullify_row(i, return_matrix)

    for i, is_zero in enumerate(zero_cols):
        if is_zero:
            nullify_cols(i, return_matrix)

    return return_matrix


class TestZeroMatrix(unittest.TestCase):
    test_data = [
        (
            [[1, 4, 5, 2, 4], [7, 2, 8, 3, 0], [4, 2, 6, 1, 2], [0, 3, 5, 2, 9]],
            [[0, 4, 5, 2, 0], [0, 0, 0, 0, 0], [0, 2, 6, 1, 0], [0, 0, 0, 0, 0]],
        )
    ]

    def test_with_test_data(self):
        for test, result in TestZeroMatrix.test_data:
            self.assertEqual(zero_matrix(test), result)


if __name__ == "__main__":
    unittest.main()
