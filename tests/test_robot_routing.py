import pytest
import math
from ..robot_routing.world import *
from ..robot_routing.robot_routing import *


def test_sample1():
    origin = (2, 3)
    destination = (8, 1)
    barriers = [(8, 2), (7, 1), (4, 5)]
    lasers = [(9, 5, 'N')]
    wormhole_pairs = [[(2, 2), (10, 1)]]

    # small difference from the given sample but with the same number of steps
    # [(2, 3), (3, 3), (3, 2), ...]
    #  vs
    # [(2, 3), (2, 2), (2, 1), ...]
    #
    expected = [(2, 3), (3, 3), (3, 2), (10, 1), (9, 1), (8, 1)]

    world = World(origin, destination, barriers, lasers, wormhole_pairs)
    actual = RobotRouting(world).get_shortest_path()

    assert expected == actual


def test_problem1():
    origin = (2, 3)
    destination = (8, 1)
    barriers = [(8, 2), (7, 1), (8, 0), (9, 2), (10, 2)]
    lasers = []
    wormhole_pairs = []

    expected = [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0), (7, -1), (8, -1), (9, -1), (9, 0), (9, 1), (8, 1)]

    world = World(origin, destination, barriers, lasers, wormhole_pairs)
    actual = RobotRouting(world).get_shortest_path()

    assert expected == actual


def test_problem2():
    origin = (2, 3)
    destination = (8, 1)
    barriers = [(8, 2), (7, 1), (8, 0), (9, 2), (10, 2)]
    lasers = [(11, 5, 'S'), (6, 0, 'N')]
    wormhole_pairs = []

    expected = [(2, 3), (3, 3), (4, 3), (5, 3), (5, 2), (5, 1), (5, 0), (5, -1), (6, -1), (7, -1), (8, -1), (9, -1), (9, 0), (9, 1), (8, 1)]

    world = World(origin, destination, barriers, lasers, wormhole_pairs)
    actual = RobotRouting(world).get_shortest_path()

    assert expected == actual


def test_problem3():
    origin = (2, 3)
    destination = (8, 1)
    barriers = [(8, 2), (7, 1), (8, 0), (9, 2), (10, 2), (11, 2), (12, 1), (12, 0), (11, 0), (10, 0), (9, 0)]
    lasers = [(11, 5, 'S'), (6, 0, 'N')]
    wormhole_pairs = [[(11, 1), (11, 6)]]

    expected = [(2, 3), (3, 3), (4, 3), (5, 3), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (10, 5), (10, 6), (11, 1), (10, 1), (9, 1), (8, 1)]

    world = World(origin, destination, barriers, lasers, wormhole_pairs)
    actual = RobotRouting(world).get_shortest_path()

    assert expected == actual

def test_problem4():
    origin = (10, 4)
    destination = (0, 8)
    barriers = [(4, 7), (9, 3), (9, 2), (10, 1), (11, 2), (11, 3), (12, 4)]
    lasers = [(10, 7, 'E')]
    wormhole_pairs = [[(10, 2), (0, 7)]]

    expected = [(10, 4), (9, 4), (8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4), (3, 5), (3, 6), (2, 6), (2, 7), (1, 7), (1, 8), (0, 8)]

    world = World(origin, destination, barriers, lasers, wormhole_pairs)
    actual = RobotRouting(world).get_shortest_path()

    assert expected == actual
