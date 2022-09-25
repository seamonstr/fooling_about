def urlify(input: str, length: int) -> str:
    dest = len(str) - 1
    i = length - 1

    while i >= 0:
        if input[i] == ' ':
            dest -= 2
            input[dest:3] = '%20'
        else:
            input[dest] = input[i]
        i -= 1
        dest -= 1
    return
