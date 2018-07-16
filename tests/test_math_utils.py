import pytest
from ..robot_routing.math_utils import *
from ..robot_routing.points import Point


@pytest.mark.parametrize("xa, ya, xb, yb, expected", [
    (0, 0, 0, 1, 1),
    (0, 0, 1, 0, 1),
    (1, 0, 0, 0, 1),
    (0, 1, 0, 0, 1),
    (0, 0, 1, 1, 1.4142135623730951),
    (1, 1, 0, 0, 1.4142135623730951)
])
def test_distance_between_points(xa,ya,xb,yb,expected):
    actual = distance_between_points(Point(xa,ya), Point(xb,yb))
    assert expected == actual
