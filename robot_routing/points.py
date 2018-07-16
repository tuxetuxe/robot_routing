class BoundedBox:
    def __init__(self, bottom_left, top_right):
        self.bottom_left = bottom_left
        self.top_right = top_right

    def is_point_inside(self, point):
        return self.bottom_left.x <= point.x <= self.top_right.x and \
               self.bottom_left.y <= point.y <= self.top_right.y

    def __str__(self):
        return "(x > %d and x < %d), (y > %d and y < %d)" % (self.bottom_left.x,
                                                             self.top_right.x,
                                                             self.bottom_left.y,
                                                             self.top_right.y)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_neighbors(self):
        return [Point(self.x + 1, self.y),
                Point(self.x, self.y - 1),
                Point(self.x - 1, self.y),
                Point(self.x, self.y + 1),
               ]

    def to_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(%3d, %3d)" % (self.x, self.y)

    def __hash__(self):
        return hash("%d:%d" % (self.x, self.y))
