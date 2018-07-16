import argparse
import math_utils
import file_utils
from world import World
import world
import heapq

class NodeQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]

def compute_shortest_path(world):

    nodes_to_visit = NodeQueue()
    nodes_to_visit.put(world.origin, 0)

    destination = world.destination

    while not nodes_to_visit.is_empty():
        current_node = nodes_to_visit.pop()
        current_tick = current_node.visited_on_tick + 1

        # print("\n\nCurrent Node: %s" % current_node)

        if current_node == destination:
            break

        for neighbor_node in world.get_neighbors(current_node, current_tick):
            cost = current_node.cost + world.movement_cost(neighbor_node, current_tick)
            need_to_visit_neighbor = cost != math_utils.INFINITY and (neighbor_node.cost is None or cost < neighbor_node.cost)

            # print("Neighbor Node: %s" % neighbor_node)
            # print("\t cost: %s; will visit: %r" % ( str(cost), need_to_visit_neighbor) )

            if need_to_visit_neighbor:
                neighbor_node.cost = cost
                neighbor_node.previous_node = current_node
                neighbor_node.visited_on_tick = current_tick
                distance_to_destination = math_utils.distance_between_points(neighbor_node.point, destination.point)
                queue_weight = cost + distance_to_destination
                nodes_to_visit.put(neighbor_node, queue_weight)

    return build_solution_path(world)


def build_solution_path(world):
    path = []
    if world.destination.previous_node is not None:
        node = world.destination

        while node is not None:
            path.insert(0, node.point.to_tuple())
            node = node.previous_node

    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_file', help='The input problem text file')
    parser.add_argument('solution_file', help='The output solution text file')
    args = parser.parse_args()

    print("Loading the problem from %s " % args.problem_file)
    world = file_utils.read_world_from_problem_file(args.problem_file)

    print("World configuration at start:")
    for (k,v) in world.nodes.iteritems():
        print(str(v))
    print("World boundaries: %s" % world.boundaries)

    print("Calculating shortest path between %s and %s" % (world.origin.point, world.destination.point))
    solution_path = compute_shortest_path(world)

    #print("World configuration at end:")
    #for (k,v) in world.nodes.iteritems():
    #    print(str(v))

    print("Solution path:")
    print(solution_path)

    print("Solution path length: %d" % len(solution_path))

    print("Writing solution to %s " % args.solution_file)
    file_utils.write_solution_file(args.solution_file, solution_path)
