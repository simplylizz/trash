# Problem Description
# Calculate the volume of water that will be caught between towers.
# Imagine a row of three towers:
#   #
#   # #
#   ###
# If water is poured over the towers, water will be caught between the two towers on the edges.
# If each # is 1 unit by 1 unit, then 1 unit of water will be caught.
#    #
#    #  #
#  # #  ##
#  #########
# In this example there are two troughs. The first on the left captures 1 unit of water,
# while the other trough captures 4 units for a total of 5 units of water.
#
# Write a function that will perform this calculation.
#
# Inputs
# towers an array of non-negative integers representing the height of the row of towers
#
# Outputs
# the volume of water the row of towers will catch


def get_volume(level, towers_arr):
    start = None
    for i, el in enumerate(towers_arr):
        if level <= el:
            if start is None:
                start = i
            else:
                yield i - start - 1
                start = i


def solution(towers_arr):
    total_water = 0

    level = 1
    while any(e >= level for e in towers_arr):
        water = sum(get_volume(level, towers_arr))
        #print(water, level)
        total_water += water
        level += 1

    return total_water


def solution2(towers_arr):
    left = []
    max_el = towers_arr[0]
    for el in towers_arr:
        if el > max_el:
            max_el = el
        left.append(max_el)

    right = []
    max_el = towers_arr[-1]
    for el in towers_arr[::-1]:
        if el > max_el:
            max_el = el
        right.append(max_el)
    right = right[::-1]

    # print(f"left: {left}\nright: {right}")

    water = 0
    for el, left_max, right_max in zip(towers_arr, left, right):
        height = min(left_max, right_max)
        diff = height - el
        if diff > 0:
            water += diff

    return water


print(solution([0, 3, 1, 2]))
print(solution([2, 1, 4, 1, 1, 3, 2, 1, 1]))


print(solution2([0, 3, 1, 2]))
print(solution2([2, 1, 4, 1, 1, 3, 2, 1, 1]))