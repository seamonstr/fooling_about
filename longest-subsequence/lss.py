def longest_subsequence(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0

    if a[-1] == b[-1]:
        return 1 + longest_subsequence(a[:-1], b[:-1])
    else:
        return max(longest_subsequence(a[:-1], b), longest_subsequence(a, b[:-1]))


def _brute_force(a, b):
    # For all possible subsequences of a
    longest = 0
    for i in range(1, pow(2, len(a))):
        seq = _array_for_mask(a, i)
        if longest < len(seq) and _brute_force_is_subseq_of(seq, b):
            longest = len(seq)
    return longest


def _array_for_mask(arr, mask):
    """
        mask is a bit mask, with each bit indicating an element number in array.
        The return value is a subsquence of arr containing each element in arr
        whose corresponding bit is set on.
    """
    ret = []
    inx = 0
    while mask != 0:
        if mask & 1 == 1:
            ret += [arr[inx]]
        inx += 1
        mask = mask >> 1

    return ret


def _brute_force_is_subseq_of(subseq, arr):
    current = 0

    if not subseq:
        return True

    for i in arr:
        if subseq[current] == i:
            current += 1
            if current == len(subseq):
                return True

    return False


def _dynamic_is_subseq_of(subseq, from_, arr):
    if len(subseq) > 1:
        midpoint = len(subseq) // 2
        first_half = subseq[0: midpoint]
        second_half = subseq[midpoint:]

        first_half_pos = _dynamic_is_subseq_of(first_half, from_, arr)
        if (first_half_pos != -1 and
                _dynamic_is_subseq_of(second_half, first_half_pos
                        + len(first_half), arr) != -1):
            return first_half_pos
    elif len(subseq) == 0:
        return 0
    else:
        for i in range(from_, len(arr)):
            if arr[i] == subseq[0]:
                return i

    return -1
