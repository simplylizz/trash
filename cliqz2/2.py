

def solution(K, A):
    """
    >>> solution(6, [-3, -2, 0, 1, 1, 3, 4, 5, 8])
    """
    A.sort()

    pairs = 0

    i = 0
    j = len(A) - 1

    while i < len(A):
        sum_ = A[i] + A[j]

        print i, j, pairs, sum_

        if sum_ == K:
            pairs += 2 if i != j else 1

            if A[j-1] == A[j]:
                j -= 1
            else:
                i += 1
        elif sum_ < K:
            i += 1
        else:
            j -= 1

    return pairs


solution(6, [1, 8, -3, 0, 1, 3, -2, 4, 5])
