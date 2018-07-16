import pytest
from ..robot_routing.nodes import *


@pytest.mark.parametrize("node, expected", [
    (Node(0, 0), 1),
    (Origin(0, 0), 1),
    (Destination(0, 0), 1),
    (EmptyNode(0, 0), 1),
    (Barrier(0, 0), math.inf),
    (Laser(0, 0, 'N'), math.inf),
    (Wormhole(0, 0, 1, 1), 1)
])
def test_movement_cost(node,expected):
    actual = node.movement_cost()
    assert expected == actual


@pytest.mark.parametrize("lx, ly, initial_direction, tick, expected", [
    (0, 0, 'N', 0, 'N'),
    (0, 0, 'N', 1, 'E'),
    (0, 0, 'N', 2, 'S'),
    (0, 0, 'N', 3, 'W'),
    (0, 0, 'N', 4, 'N'),
    (0, 0, 'E', 0, 'E'),
    (0, 0, 'E', 1, 'S'),
    (0, 0, 'E', 2, 'W'),
    (0, 0, 'E', 3, 'N'),
    (0, 0, 'E', 4, 'E'),
    (0, 0, 'S', 0, 'S'),
    (0, 0, 'S', 1, 'W'),
    (0, 0, 'S', 2, 'N'),
    (0, 0, 'S', 3, 'E'),
    (0, 0, 'S', 4, 'S'),
    (0, 0, 'W', 0, 'W'),
    (0, 0, 'W', 1, 'N'),
    (0, 0, 'W', 2, 'E'),
    (0, 0, 'W', 3, 'S'),
    (0, 0, 'W', 4, 'W')
])
def test_laser_direction_on_tick(lx, ly, initial_direction, tick, expected):
    actual = Laser(lx, ly, initial_direction).get_direction_on_tick(tick)
    assert expected == actual


@pytest.mark.parametrize("lx, ly, direction, px, py, tick, barriers, expected", [
    (0, 0, 'N', 0, 1, 0, [], True),
    (0, 0, 'N', 0, -1, 0, [], False),
    # diagonal cells are never hit by the laser
    (0, 0, 'N', 1, 1, 0, [], False),
    (0, 0, 'N', 1, 1, 1, [], False),
    (0, 0, 'N', 1, 1, 2, [], False),
    (0, 0, 'N', 1, 1, 3, [], False),
    (0, 0, 'N', 1, 1, 4, [], False),
    # test rotation of laser
    (0, 0, 'N', 1, 0, 0, [], False),
    (0, 0, 'N', 1, 0, 1, [], True),
    (0, 0, 'N', 1, 0, 2, [], False),
    (0, 0, 'N', 1, 0, 3, [], False),
    (0, 0, 'N', 1, 0, 4, [], False),
    (0, 0, 'N', 1, 0, 5, [], True),
    # test barrier blocking
    (0, 0, 'N', 0, 2, 0, [Barrier(0, 1)], False),
    (0, 0, 'N', 0, 2, 0, [Barrier(0, 3)], True),
    (0, 0, 'N', 0, 2, 0, [Barrier(0, -1)], True),
    (0, 0, 'N', 0, 2, 0, [Barrier(1, 0)], True),
    (0, 0, 'N', 0, 3, 0, [Barrier(0, 1), Barrier(0, 2)], False),
    (0, 0, 'E', 2, 0, 0, [Barrier(1, 0)], False),
    (0, 0, 'E', 2, 0, 0, [Barrier(3, 0)], True),
    (0, 0, 'E', 2, 0, 0, [Barrier(-1, 0)], True),
    (0, 0, 'E', 2, 0, 0, [Barrier(0, 1)], True),
    (0, 0, 'E', 3, 0, 0, [Barrier(1, 0), Barrier(2, 0)], False),
    (0, 0, 'S', 0, -2, 0, [Barrier(0, -1)], False),
    (0, 0, 'S', 0, -2, 0, [Barrier(0, -3)], True),
    (0, 0, 'S', 0, -2, 0, [Barrier(0, 1)], True),
    (0, 0, 'S', 0, -2, 0, [Barrier(-1, 0)], True),
    (0, 0, 'S', 0, -3, 0, [Barrier(0, -1), Barrier(0, -2)], False),
    (0, 0, 'W', -2, 0, 0, [Barrier(-1, 0)], False),
    (0, 0, 'W', -2, 0, 0, [Barrier(-3, 0)], True),
    (0, 0, 'W', -2, 0, 0, [Barrier(1, 0)], True),
    (0, 0, 'W', -2, 0, 0, [Barrier(0, -1)], True),
    (0, 0, 'W', -3, 0, 0, [Barrier(-1, 0), Barrier(-2, 0)], False)

])
def test_is_point_in_laser_beam(lx, ly, direction, px, py, tick, barriers, expected):
    actual = Laser(lx, ly, direction).is_point_inside_beam(Point(px, py), tick, barriers)
    assert expected == actual

@pytest.mark.parametrize("tick, expected", [
    (0, True),
    (1, False),
    (2, False),
    (3, True),
    (4, False),
    (5, False),
    (6, True),
    (7, False),
])
def test_wormhole_is_active(tick, expected):
    actual = Wormhole.is_active(tick)
    assert expected == actual