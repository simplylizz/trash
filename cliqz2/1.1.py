

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
    >>> solution([2,-2,-1])
    3
    """
    jumps = 0
    next_index = 0
    len_ = len(A)

    while 0 <= next_index < len_:
        val = A[next_index]

        if val == 0:
            return -1

        A[next_index] = 0
        next_index += val
        jumps += 1

    return jumps


if __name__ == '__main__':
    import doctest
    doctest.testmod()
