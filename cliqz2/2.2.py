import collections


def solution1(K, A):
    """
    >>> solution(6, [-3, -2, 0, 1, 1, 3, 4, 5, 8])
    """
    A.sort()

    pairs = 0

    i = 0
    j = len(A) - 1

    while i < len(A):
        sum_ = A[i] + A[j]

        #print i, j, pairs, sum_

        if sum_ == K:
            pairs += 2

            if A[j-1] == A[j]:  # out of bounds!
                j -= 1
            else:
                i += 1
        elif sum_ < K:
            i += 1
        else:
            j -= 1

    return pairs


def solution(K, A):
    """
    >>> solution(6, [-3, -2, 0, 1, 1, 3, 4, 5, 8])
    """

    counter = collections.Counter(A)

    comp_indexes = 0

    for k in counter.keys():
        v = counter.pop(k)

        # number of placements of n elements on k places:
        # Ank = n! / (n - k)!
        # and with duplicates:
        # Ank = n ** k
        if k + k == K:
            comp_indexes += v * v

        for sub_key, sub_value in counter.iteritems():
            if sub_key + k == K:
                comp_indexes += v * sub_value * 2

    return comp_indexes


print solution(6, [1, 8, -3, 0, 1, 3, -2, 4, 5])
print solution(4, [2])
print solution(4, [2, 2])
print solution(4, [2, 2, 2])
print solution(4, [2, 2, 2, 2])
print solution(4, [2, 2, 2, 2])
print solution(0, [0, 0, 0, 0])

print '######################'

print solution1(6, [1, 8, -3, 0, 1, 3, -2, 4, 5])
print solution1(4, [2])
print solution1(4, [2, 2])
print solution1(4, [2, 2, 2])
print solution1(4, [2, 2, 2, 2])
print solution1(4, [2, 2, 2, 2])
print solution1(0, [0, 0, 0, 0])
