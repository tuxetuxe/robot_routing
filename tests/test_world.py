import pytest
import math
from ..robot_routing.world import *
from ..robot_routing.nodes import *
from ..robot_routing.points import *


def build_world(origin = (0,0),
                destination = (10,10),
                barriers = [],
                lasers = [],
                wormhole_pairs = []
                ):
    return World(origin, destination, barriers, lasers, wormhole_pairs)


@pytest.mark.parametrize("world, node, tick, expected", [
    (build_world(), EmptyNode(0,0), 0, 1),
    (build_world(), Origin(0,0), 0, 1),
    (build_world(), Destination(0,0), 0, 1),
    (build_world(), Barrier(0,0), 0, math.inf),
    (build_world(), Laser(0,0, 'N'), 0, math.inf),
    (build_world(), Wormhole(0,0,1,1), 0, 1),
    (build_world(lasers=[(1,1,'N')]), EmptyNode(1,5), 0, math.inf),
    (build_world(lasers=[(1,1,'N')]), EmptyNode(1,5), 1, 1),
    (build_world(lasers=[(1,1,'N')], barriers=[(1,3)]), EmptyNode(1,5), 1, 1)
])
def test_movement_cost(world, node, tick, expected):
    actual = world.movement_cost(node, tick)
    assert expected == actual

@pytest.mark.parametrize("world, node, tick, expected", [
    (build_world(), EmptyNode(1,1), 0, [EmptyNode(2,1), EmptyNode(1,0), EmptyNode(0,1), EmptyNode(1,2)]),
    (build_world(destination=(1,1)), EmptyNode(2,2), 0, [EmptyNode(2,1), EmptyNode(1,2)]),
    (build_world(destination=(1,1)), EmptyNode(-1,-1), 0, [EmptyNode(0,-1), EmptyNode(-1,0)]),
    (build_world(wormhole_pairs=[[(2,1),(9,9)]]), EmptyNode(1,1), 0, [EmptyNode(9,9), EmptyNode(1,0), EmptyNode(0,1), EmptyNode(1,2)]),
])
def test_get_neighbors(world, node, tick, expected):
    actual = world.get_neighbors(node, tick)
    assert expected == actual


@pytest.mark.parametrize("world, px, py, expected", [
    (build_world(), 0, 0, Origin(0,0)),
    (build_world(), 10, 10, Destination(10,10)),
    (build_world(), 1, 1, EmptyNode(1,1)),
])
def test_get_node_at(world, px, py, expected):
    point = Point(px, py)
    actual = world.get_node_at(point)
    assert expected == actual
    assert world.nodes.get(point) == expected


def test_build_world():
    origin = (0, 0)
    destination = (10, 10)
    barriers = [(1,1)]
    lasers = [(2,2,'N')]
    wormhole_pairs = [[(2,1),(9,9)]]
    world = World(origin, destination, barriers, lasers, wormhole_pairs)

    assert Origin(0,0) == world.nodes.get(Point(0,0))
    assert Destination(10, 10) == world.nodes.get(Point(10,10))
    assert Barrier(1, 1) == world.nodes.get(Point(1,1))
    assert Laser(2, 2, 'N') == world.nodes.get(Point(2,2))
    assert Wormhole(2,1,9,9) == world.nodes.get(Point(2,1))
    assert Wormhole(9, 9, 2, 1) == world.nodes.get(Point(9,9))
    assert Point(-10,-10) == world.boundaries.bottom_left
    assert Point(20,20) == world.boundaries.top_right
