# O(n) implementation
def is_unique_n(str_: str) -> bool:
    seen = set()
    for c in str_:
        if c in seen:
            return False
        seen.add(c)
    return True


def is_unique_n_squared(str_: str) -> bool:
    for i, c in enumerate(str_):
        for j in str_[0:i]:
            if j == c:
                return False
    return True
