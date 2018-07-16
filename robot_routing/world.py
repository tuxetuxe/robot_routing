from nodes import *
from points import Point, BoundedBox


class World:
    def __init__(self, origin, destination, barriers = [], lasers = [], wormhole_pairs = []):
        self.origin = Origin(origin[0],origin[1])
        self.destination = Destination(destination[0],destination[1])

        self.barriers = [Barrier(n[0], n[1]) for n in barriers]
        self.lasers = [Laser(n[0], n[1], n[2]) for n in lasers]
        wormholes = [Wormhole(o[0], o[1], d[0], d[1]) for [o, d] in wormhole_pairs] + \
                    [Wormhole(d[0], d[1], o[0], o[1]) for [o, d] in wormhole_pairs]

        self.nodes = dict()
        self.nodes[self.origin.point] = self.origin
        self.nodes[self.destination.point] = self.destination
        self.add_nodes_to_dict(self.barriers)
        self.add_nodes_to_dict(self.lasers)
        self.add_nodes_to_dict(wormholes)

        min_x = min([p.x for p in self.nodes.iterkeys()])
        min_y = min([p.y for p in self.nodes.iterkeys()])

        max_x = max([p.x for p in self.nodes.iterkeys()])
        max_y = max([p.y for p in self.nodes.iterkeys()])

        #
        # Adding an "border" to the possible search space so the robot can potentially go around any node in the edge
        # and evade the lasers even if that takes a bit longer
        #
        map_border = max((max_x - min_x), (max_y - min_y))

        self.boundaries = BoundedBox(Point(min_x - map_border, min_y - map_border),
                                     Point(max_x + map_border, max_y + map_border))

    def add_nodes_to_dict(self, nodes_list):
        self.nodes.update(dict((n.point, n) for n in nodes_list))

    def get_node_at(self, point):
        if not point in self.nodes:
            self.nodes[point] = EmptyNode(point.x, point.y)
        return self.nodes.get(point)

    def get_neighbors(self, node, tick):
        node_point = node.point

        valid_neighbors = []
        neighbor_points = node_point.get_neighbors()

        for point in neighbor_points:
            if self.boundaries.is_point_inside(point):
                node = self.get_node_at(point)

                # if an wormhole is active in this tick the robot is not really there but on the other side
                if isinstance(node, Wormhole) and Wormhole.is_active(tick):
                    node = self.get_node_at(node.destination_point)

                valid_neighbors.append(node)

        return valid_neighbors

    def movement_cost(self, node, tick):
        is_in_laser_beam = any([laser.is_point_inside_beam(node.point, tick, self.barriers) for laser in self.lasers])
        if is_in_laser_beam:
            return INFINITY
        else:
            return node.movement_cost()
