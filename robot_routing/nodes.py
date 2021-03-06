from points import *
import math

CLOCKWISE_DIRECTIONS_MAP = {'N': 'E',
                            'E': 'S',
                            'S': 'W',
                            'W': 'N'
                            }

WORMHOLE_FREQUENCY = 3


class Node:
    def __init__(self, x, y, cost=None, previous_node=None, visited_on_tick=None):
        self.point = Point(x, y)
        self.cost = cost
        self.previous_node = previous_node
        self.visited_on_tick = visited_on_tick

    @staticmethod
    def can_move_into():
        return True

    def __eq__(self, other):
        return self.point == other.point

    def __lt__(self, other):
        return self.cost < other.cost

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "point: %s; visited on: %s; cost: %s; from: %s" % (str(self.point),
                                                                  str(self.visited_on_tick),
                                                                  str(self.cost),
                                                                  'None' if self.previous_node is None else str(self.previous_node.point)
                                                                  )


class Origin(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y, 0, None, 0)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[ORIGIN     ] %s" % Node.__str__(self)


class Destination(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y, None, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[DESTINATION] %s" % Node.__str__(self)


class EmptyNode(Node):
    def __init__(self, x, y, cost=None, previous_node=None):
        Node.__init__(self, x, y, cost, previous_node)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[           ] %s" % Node.__str__(self)


class Barrier(Node):
    def __init__(self, x, y):
        Node.__init__(self, x, y, math.inf)

    @staticmethod
    def can_move_into():
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[BARRIER    ] %s" % Node.__str__(self)


class Laser(Node):
    def __init__(self, x, y, initial_direction):
        Node.__init__(self, x, y, -math.inf)
        self.initial_direction = initial_direction

    @staticmethod
    def can_move_into():
        return False

    def get_direction_on_tick(self, tick):
        direction = self.initial_direction
        rotations = tick % 4

        for _ in range(rotations):
            direction = CLOCKWISE_DIRECTIONS_MAP[direction]

        return direction

    def is_point_inside_beam(self, point, tick, barriers):
        direction = self.get_direction_on_tick(tick)
        if direction == 'N':
            is_blocked_by_barrier = any([self.point.x == b.point.x and self.point.y < b.point.y < point.y for b in barriers])
            return point.x == self.point.x and point.y >= self.point.y and not is_blocked_by_barrier
        if direction == 'E':
            is_blocked_by_barrier = any([self.point.y == b.point.y and self.point.x < b.point.x < point.x for b in barriers])
            return point.y == self.point.y and point.x >= self.point.x and not is_blocked_by_barrier
        if direction == 'S':
            is_blocked_by_barrier = any([self.point.x == b.point.x and self.point.y > b.point.y > point.y for b in barriers])
            return point.x == self.point.x and point.y <= self.point.y and not is_blocked_by_barrier
        if direction == 'W':
            is_blocked_by_barrier = any([self.point.y == b.point.y and self.point.x > b.point.x > point.x for b in barriers])
            return point.y == self.point.y and point.x <= self.point.x and not is_blocked_by_barrier

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[LASER      ] %s; initial_direction: %s" % (Node.__str__(self), self.initial_direction)


class Wormhole(Node):
    def __init__(self, x, y, destination_x, destination_y):
        Node.__init__(self, x, y)
        self.destination_point = Point(destination_x, destination_y)

    @staticmethod
    def is_active(tick):
        return tick % WORMHOLE_FREQUENCY == 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[WORMHOLE   ] %s; destination: %s" % (Node.__str__(self), str(self.destination_point))
