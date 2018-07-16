import math


def distance_between_points(point_a, point_b):
    return math.sqrt((point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2)
