

def solution(A):
    """
    >>> solution([1,1,1])
    3
    >>> solution([3,2,1])
    1
    >>> solution([2,2,1])
    2
    >>> solution([1,1,-2])
    -1
    >>> solution([-100,1,-2])
    1
    >>> solution([100,1,-2])
    1
    """

    visited = set()

    jumps = 0
    next_index = 0

    while True:
        try:
            visited.add(next_index)
            next_index += A[next_index]
            if next_index in visited:
                return -1
            else:
                jumps += 1
        except IndexError:
            return jumps


if __name__ == '__main__':
    import doctest
    doctest.testmod()
