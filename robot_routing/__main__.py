import argparse
import file_utils
from robot_routing import RobotRouting

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_file', help='The input problem text file')
    parser.add_argument('solution_file', help='The output solution text file')
    args = parser.parse_args()

    print("\nLoading the problem from %s " % args.problem_file)
    world = file_utils.read_world_from_problem_file(args.problem_file)

    print("\nWorld configuration at start:")
    for (k,v) in world.nodes.items():
        print(str(v))
    print("\nWorld boundaries: %s" % world.boundaries)

    print("\nCalculating shortest path between %s and %s" % (world.origin.point, world.destination.point))
    solution_path = RobotRouting(world).get_shortest_path()

    #print("World configuration at end:")
    #for (k,v) in world.nodes.iteritems():
    #    print(str(v))

    print("\nSolution path:")
    print(solution_path)

    print("\nSolution path length: %d" % len(solution_path))

    print("\nWriting solution to %s " % args.solution_file)
    file_utils.write_solution_file(args.solution_file, solution_path)
