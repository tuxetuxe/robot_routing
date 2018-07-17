import heapq
import math
import math_utils


class NodeQueue:
    """ A wrapper around python's priority queue (heapq)
    """

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
        """Computes the shortest path between the origin and destination in the world using a A* algorithm implementation
            This will change the nodes in the world so that the path can be retrieved following back from the destination
            to the origin
        """
        nodes_to_visit = NodeQueue()
        nodes_to_visit.put(self.world.origin, 0)

        destination = self.world.destination

        destination_cost = math.inf

        while not nodes_to_visit.is_empty():
            current_node = nodes_to_visit.pop()
            current_tick = current_node.visited_on_tick + 1

            if current_node == destination:
                # keep track of the current destination cost so that we don't explore nodes in the map unnecessarily
                # (ie: the cost to arrive at that node is already more than arriving at the destination
                destination_cost = destination.cost
                break

            for neighbor_node in self.world.get_neighbors(current_node, current_tick):
                if not neighbor_node.can_move_into():
                    continue

                cost = current_node.cost + self.world.movement_cost(neighbor_node, current_tick)
                need_to_visit_neighbor = cost != math.inf and cost < destination_cost and (neighbor_node.cost is None or cost < neighbor_node.cost)

                if need_to_visit_neighbor:
                    # Update the node with the new info
                    neighbor_node.cost = cost
                    neighbor_node.previous_node = current_node
                    neighbor_node.visited_on_tick = current_tick

                    # The cost is the g component in the algorithm
                    # The linear distance to the destination is the h component
                    distance_to_destination = math_utils.distance_between_points(neighbor_node.point, destination.point)
                    queue_weight = cost + distance_to_destination

                    # Add the node to the list to be visited [potentially again...]
                    nodes_to_visit.put(neighbor_node, queue_weight)

    def get_shortest_path(self):
        """Computes the shortest path in the world (see compute_shortest_path) and returns a list of tuples that represent
            the computed path
        """
        self.compute_shortest_path()
        path = []
        destination = self.world.destination
        if destination.previous_node is not None:
            node = destination

            while node is not None:
                path.insert(0, node.point.to_tuple())
                node = node.previous_node

        return path
