import unittest


def mergesort(data):
    data = data.copy()
    helper = [None] * len(data)
    mergesort_region(0, len(data) - 1, data, helper)
    return data


def mergesort_region(lo: int, hi: int, data: list[int], helper: list[int]):
    if hi <= lo:
        return
    mid = lo + (hi - lo) // 2
    mergesort_region(lo, mid, data, helper)
    mergesort_region(mid + 1, hi, data, helper)
    merge(lo, mid, hi, data, helper)


def merge(lo: int, mid: int, hi: int, data: list[int], helper: list[int]):
    print(f"lo: {lo}, mid:{mid}, hi: {hi}, region: {data[lo:hi+1]}")
    helper[lo : hi + 1] = data[lo : hi + 1]
    left_index = lo
    right_index = mid + 1
    current = lo

    while left_index <= mid and right_index <= hi:
        if helper[left_index] <= helper[right_index]:
            data[current] = helper[left_index]
            left_index += 1
        else:
            data[current] = helper[right_index]
            right_index += 1
        current += 1

    # Copy the remains of left
    remain = mid - left_index
    for i in range(remain + 1):
        data[current + i] = helper[left_index + i]
    print(data[lo : hi + 1])


class TestMergeSort(unittest.TestCase):
    testcases = [
        [[4, 1, 2, 5, 3], [1, 2, 3, 4, 5]],
        [[5, 4, 3, 2, 1], [1, 2, 3, 4, 5]],
        [[], []],
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 1000, 0, 0, 0], [0, 0, 0, 0, 1000]],
    ]

    def test_happy_path(self):
        for i in TestMergeSort.testcases:
            self.assertEqual(mergesort(i[0]), i[1])


if __name__ == "__main__":
    unittest.main()
