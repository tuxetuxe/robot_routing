import pytest
from ..robot_routing.points import *


@pytest.mark.parametrize("box, px, py, expected", [
    (BoundedBox(Point(0,0), Point(1,1)), 0, 0, True),
    (BoundedBox(Point(0,0), Point(1,1)), 0, 1, True),
    (BoundedBox(Point(0,0), Point(1,1)), 1, 0, True),
    (BoundedBox(Point(0,0), Point(1,1)), 1, 1, True),
    (BoundedBox(Point(0,0), Point(1,1)), 2, 2, False),
    (BoundedBox(Point(0,0), Point(1,1)), -2, -2, False),
    (BoundedBox(Point(0,0), Point(10,10)), 5, 5, True)
])
def test_is_inside_bonded_box(box, px, py, expected):
    actual = box.is_point_inside(Point(px, py))
    assert expected == actual


def test_neighbor_points():
    point = Point(0,0)
    expected = [Point(1,0),Point(0,-1),Point(-1,0),Point(0,1)]
    actual = point.get_neighbors()
    assert expected == actual

@pytest.mark.parametrize("ax, ay, bx, by, expected", [
    (0, 0, 0, 0, True),
    (0, 1, 0, 1, True),
    (1, 0, 1, 0, True),
    (1, 0, 0, 0, False),
    (0, 1, 0, 0, False),
    (1, 1, 0, 0, False),
    (0, 0, 0, 1, False),
    (0, 0, 1, 0, False),
    (0, 0, 1, 1, False)
])
def test_equals(ax, ay, bx, by, expected):
    actual = Point(ax,ay).__eq__(Point(bx, by))
    assert expected == actual


def test_to_tuple():
    expected = (1234,1234)
    actual = Point(1234,1234).to_tuple()
    assert expected == actual


def test_hash():
    expected = hash("1234:1234")
    actual = Point(1234,1234).__hash__()
    assert expected == actual