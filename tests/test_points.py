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