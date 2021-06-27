import collections


def fibonacci(n):
    """
    >>> fibonacci(1)
    [0]
    >>> fibonacci(8)
    [0, 1, 1, 2, 3, 5, 8, 13]
    """
    res = []

    a = 0
    b = 1

    for _ in range(n):
        res.append(a)

        a, b = b, a + b

    return res