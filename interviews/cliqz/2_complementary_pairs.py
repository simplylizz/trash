import collections


def solution(k, v):
    vmap = collections.Counter(v)

    pairs = 0

    for key, value in vmap.items():
        if k - key in vmap:
            pairs += value * vmap[k-key]

    return pairs


if __name__ == '__main__':
    # print("1. Expected 0, got ", solution(1, [1]))

    # print("2. Expected 2, got ", solution(3, [1, 2]))

    print("3. Expected 4, got ", solution(2, [1, 1]))

    # print("4. Expected 0, got ", solution(99, [1, 2, 3, 4]))

    # print("5. Expected 4, got ", solution(5, [1, 2, 3, 3]))

    # print("6. Expected 9, got ", solution(6, [3, 3, 3]))

    # print("7. Expected 6, got ", solution(3, [3, 3, 3, 0]))

    # print("8. Expected 7, got ", solution(6, [1, 8, -3, 0, 1, 3, -2, 4, 5]))
