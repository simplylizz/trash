

"""
Сalculate the minimal longest jump distance for given teleports
set and destination point from (0, 0, 0) point.

The main idea:

1. Initialize cluster with (0, 0, 0) point, set max_distance = 0;
2. while dest not in cluster:
   - pick closest to the cluster point, set max_distance = distance
     to this point (i.e. distance from this point to closest point
     in the cluster);
   - add recursively each point on distance = max_distance to the
     cluster;

Time complexity for current solution:
For each point in cluster we need to:
  1. find 1 closest point;
  2. find all points in radius.
Because everything is implemented right now as a linear search, this
give us O(n^2) time complexity.

The first improvement: use R-tree/KD-tree or some other structure for
spatial data wich could give better performance on this type of
lookups:
  1. Get all points in given radius.
  2. Get (1 or N?) closest points.

Here is a nice article about them:
https://blog.mapbox.com/a-dive-into-spatial-search-algorithms-ebd0c5e39d2a

The second: we could try to use binary search to find required distance.
In the worst case max distance = distance to Zearth. So we could try to
use binary search to find a min clusterization distance with which we
could reach Zearth. In this case we need only cheap queries of type
"get all points in radius".

Another improvement which could give better performance (not in terms
of asymptotic complexity but in terms of calculations efficiency):
We could use simplified distance metric and get rid of floating point
calculations. For example: distance = abs(x1 - x2) + abs(y1 - y2).
Instead of calculating standard euclidian distance through hypot/square
roots.
"""

import math


class SpatialIndex:
    """
    A poor man's spatial index. :)
    """

    def __init__(self, points):
        self.points = set(points)

    @staticmethod
    def _calc_distance(point_1, point_2):
        return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point_1, point_2)))

    def get_closest(self, point):
        """
        return (point, distance)
        """
        min_distance = float('inf')
        min_distance_point = None

        for p in self.points:
            distance = self._calc_distance(point, p)
            if min_distance is None or min_distance > distance:
                min_distance = distance
                min_distance_point = p

        return min_distance_point, min_distance

    def get_in_radius(self, center, radius):
        """
        return [point1, point2, ...]
        """
        points = []

        for p in self.points:
            if self._calc_distance(center, p) <= radius:
                points.append(p)

        return points

    def remove(self, point):
        self.points.discard(point)


def calc_min_max_hop(teleports, dest):
    index = SpatialIndex(teleports + [dest])

    cluster = {(0, 0, 0)}
    index.remove((0, 0, 0))

    cluster_distance = 0

    queue = set()  # queue to add points into cluster
    while True:
        min_distance_point = None
        min_distance = float('inf')
        for point in cluster:
            closest_point, distance = index.get_closest(point)

            if min_distance > distance:
                min_distance_point = closest_point
                min_distance = distance

        assert min_distance_point is not None

        queue.add(min_distance_point)
        cluster_distance = max(cluster_distance, min_distance)

        if dest in cluster:
            return cluster_distance

        while queue:
            point = queue.pop()
            cluster.add(point)
            index.remove(point)

            for neighbour_point in index.get_in_radius(point, cluster_distance):
                if neighbour_point not in cluster:
                    queue.add(neighbour_point)
                    cluster.add(neighbour_point)
                    index.remove(neighbour_point)

        if dest in cluster:
            return cluster_distance


def main():
    def parse_coords(s):
        return tuple(float(x) for x in s.split(" "))

    zearth = parse_coords(input())
    teleports = [parse_coords(input()) for _ in range(int(input()))]

    distance = calc_min_max_hop(teleports=teleports, dest=zearth)
    print("{:.2f}".format(distance))


if __name__ == '__main__':
    main()
