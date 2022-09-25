import sys


def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("fib.py <fib_index>")
        sys.exit(1)
    print(fib(int(sys.argv[1])))
