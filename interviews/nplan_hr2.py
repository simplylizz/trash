

def number_of_sub_paths(a):
    row_sum = [0] * len(a[0])

    row_sum[0] = 1
    for row in range(len(a)):
        for col in range(len(a[0])):
            if row == 0 and col == 0:
                continue

            if not a[row][col]:
                row_sum[col] = 0
            else:
                if col > 0:
                    row_sum[col] += row_sum[col - 1]

    return row_sum[-1]


def numberOfPaths(a):
    """
    >>> numberOfPaths([[1, 1], [1, 1]])
    2
    >>> numberOfPaths([[1, 1], [1, 1], [1, 1]])
    3
    >>> numberOfPaths([[1] * 4] * 3)
    10
    >>> numberOfPaths([[1, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
    4
    >>> numberOfPaths([[1, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])
    6
    >>> numberOfPaths([[1, 1, 1], [0, 1, 1], [1, 1, 1]])
    3
    >>> numberOfPaths([[1, 0, 1], [1, 1, 1], [1, 1, 1]])
    3
    >>> numberOfPaths([[1] * 4] * 4)
    20
    """

    if not a[-1][-1]:  # exit is blocked, no paths
        return 0

    return number_of_sub_paths(a) % (10 ** 9 + 7)


# if __name__ == '__main__':
