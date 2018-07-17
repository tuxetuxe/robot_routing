import heapq
import math
import math_utils


class NodeQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]


class RobotRouting:
    def __init__(self, world):
        self.world = world

    def compute_shortest_path(self):
        nodes_to_visit = NodeQueue()
        nodes_to_visit.put(self.world.origin, 0)

        destination = self.world.destination

        while not nodes_to_visit.is_empty():
            current_node = nodes_to_visit.pop()
            current_tick = current_node.visited_on_tick + 1

            if current_node == destination:
                break

            for neighbor_node in self.world.get_neighbors(current_node, current_tick):
                if not neighbor_node.can_move_into():
                    continue

                cost = current_node.cost + self.world.movement_cost(neighbor_node, current_tick)
                need_to_visit_neighbor = cost != math.inf and (neighbor_node.cost is None or cost < neighbor_node.cost)

                if need_to_visit_neighbor:
                    neighbor_node.cost = cost
                    neighbor_node.previous_node = current_node
                    neighbor_node.visited_on_tick = current_tick
                    distance_to_destination = math_utils.distance_between_points(neighbor_node.point, destination.point)
                    queue_weight = cost + distance_to_destination
                    nodes_to_visit.put(neighbor_node, queue_weight)

    def get_shortest_path(self):
        self.compute_shortest_path()
        path = []
        destination = self.world.destination
        if destination.previous_node is not None:
            node = destination

            while node is not None:
                path.insert(0, node.point.to_tuple())
                node = node.previous_node

        return path
