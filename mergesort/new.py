import unittest


def mergesort(data: list[int]) -> list[int]:
    ret = data.copy()
    helper = [0] * len(ret)
    mergesort_region(0, len(ret) - 1, ret, helper)
    return ret


def mergesort_region(lo: int, hi: int, data: list[int], helper: list[int]):
    if hi <= lo:
        return
    mid = lo + (hi - lo) // 2
    mergesort_region(lo, mid, data, helper)
    mergesort_region(mid + 1, hi, data, helper)
    merge(lo, mid, hi, data, helper)


def merge(lo: int, mid: int, hi: int, data: list[int], helper: list[int]):
    helper[lo:hi + 1] = data[lo:hi + 1]

    l_inx = lo
    r_inx = mid + 1
    write_inx = lo
    while l_inx <= mid and r_inx <= hi:
        if data[l_inx] <= data[r_inx]:
            helper[write_inx] = data[l_inx]
            l_inx += 1
        else:
            helper[write_inx] = data[r_inx]
            r_inx += 1
        write_inx += 1

    while l_inx <= mid:
        helper[write_inx] = data[l_inx]
        write_inx += 1
        l_inx += 1
    data[lo:hi + 1] = helper[lo:hi + 1]


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
