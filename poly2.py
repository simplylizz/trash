

"""
1. Build an empty (i.e. filled with 0 or something like that) map of
   city.
2. For each pizzeria point inc value of cells in delivery distance and
   maintain max cell value.

Time complexity: O(n * m) where n is number of pizzerias and m is size
of map (actually m is something like "average delivery distance" but in
the worst case it equals to map size).

What could be better in the current solution: depending on pizza
delivery density we could use different data structures to store map:
1. List of lists (or maybe arrays from numpy) in case if density is
   high and almost all cells would have non-zero value.
2. I'm not sure, but maybe some kind of sparse arrays could perform
   better than dict. But that's not for sure and should be tested on
   real data patterns.

I have not idea how it could be done better.
"""

import collections


def get_range(x, y, distance):
    """Yields all coordinates inside the delivery distance"""

    c_x = x - distance

    lower_y = y
    upper_y = y + 1

    while c_x <= x + distance:
        for c_y in range(lower_y, upper_y):
            yield c_x, c_y

        c_x += 1

        if c_x <= x:
            lower_y -= 1
            upper_y += 1
        else:
            lower_y += 1
            upper_y -= 1


def calc_max_pizzeria_density(map_size, pizzerias):
    max_density = 0
    density_map = collections.defaultdict(int)

    for pizzeria in pizzerias:
        for point in get_range(*pizzeria):
            density = density_map[point] + 1
            density_map[point] = density
            if density > max_density:
                max_density = density

    return max_density


def main():
    def parse_ints(s):
        return tuple(int(x) for x in s.split(" "))

    map_size, num_pizzerias = parse_ints(input())

    pizzerias = [parse_ints(input()) for _ in range(num_pizzerias)]

    max_density = calc_max_pizzeria_density(map_size=map_size, pizzerias=pizzerias)
    print("{}".format(max_density))


if __name__ == '__main__':
    main()
