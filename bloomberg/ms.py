import random


def merge_sort(arr):
    """
    >>> merge_sort([3, 2, 1])
    [1, 2, 3]
    >>> merge_sort([2, 1, 3])
    [1, 2, 3]
    >>> merge_sort([1, 2, 3])
    [1, 2, 3]
    >>> from random import shuffle
    >>> arr = list(range(1000))
    >>> shuffle(arr)
    >>> merge_sort(arr) == list(range(1000))
    True
    """
    if len(arr) <= 1:
        return arr
    else:
        middle = len(arr) // 2
        arr1 = merge_sort(arr[:middle])
        arr2 = merge_sort(arr[middle:])
        sorted_arr = []
        for i in range(len(arr)):
            if not arr1:
                sorted_arr.append(arr2.pop(0))
            elif not arr2:
                sorted_arr.append(arr1.pop(0))
            elif arr1[0] <= arr2[0]:
                sorted_arr.append(arr1.pop(0))
            else:
                sorted_arr.append(arr2.pop(0))
        return sorted_arr


def quick_sort(arr):
    """
    >>> quick_sort([3, 2, 1])
    [1, 2, 3]
    >>> quick_sort([2, 1, 3])
    [1, 2, 3]
    >>> quick_sort([1, 2, 3])
    [1, 2, 3]
    >>> from random import shuffle
    >>> arr = list(range(1000))
    >>> shuffle(arr)
    >>> quick_sort(arr) == list(range(1000))
    True
    """
    if len(arr) <= 1:
        return arr
    else:
        # pivot_i = len(arr) // 2
        pivot_i = random.randint(0, len(arr) - 1)
        # pivot_i = len(arr) - 1
        # pivot_i = 0
        pivot = arr[pivot_i]

        l_i = 0
        arr[pivot_i], arr[-1] = arr[-1], pivot
        r_i = len(arr) - 2

        while l_i != r_i:
            if arr[l_i] > pivot:
                arr[l_i], arr[r_i] = arr[r_i], arr[l_i]
                r_i -= 1
            else:
                l_i += 1

        # put back pivot: on current left index or on the next position
        if arr[l_i] > pivot:
            arr[l_i], arr[-1] = arr[-1], arr[l_i]
        else:
            l_i += 1
            arr[l_i], arr[-1] = arr[-1], arr[l_i]
        pivot_i = l_i

        arr[:pivot_i] = quick_sort(arr[:pivot_i])
        arr[pivot_i + 1:] = quick_sort(arr[pivot_i + 1:])

        return arr
