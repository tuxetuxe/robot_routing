import argparse
import itertools
import ast
from collections import namedtuple
from copy import deepcopy
import sys

GRID_BUFFER = 3
ROBOT_CHARACTER = 'R'
LASER_CHARACTER = 'L'
LASER_BEAM_CHARACTER = '*'
WORMHOLE_CHARACTER = 'W'
OBSTACLE_CHARACTER = 'X'
ORIGIN_CHARACTER = 'o'
DESTINATION_CHARACTER = 'd'
VALID_KEYS = set(['n', 'b', 'q'])
VISUALIZE_FLAGS = set(['barriers', 'static_lasers', 'rotating_lasers', 'wormhole_pairs'])
WORMHOLE_FREQUENCY = 3
NORTH, EAST, SOUTH, WEST = 'N', 'E', 'S', 'W'
LASER_DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
Bbox = namedtuple('Bbox', ['x_min', 'y_min', 'x_max', 'y_max'])

def extract_problem_configuration(problem_file, visualization_flags):
    file_contents = []
    with open(problem_file) as f:
        file_contents = f.readlines()
    file_contents = [line.strip() for line in file_contents]
    barriers, static_lasers, rotating_lasers, wormhole_pairs = [], [], [], []
    if 'barriers' in visualization_flags:
        barriers = ast.literal_eval(file_contents[2])
    if 'static_lasers' in visualization_flags:
        static_lasers = ast.literal_eval(file_contents[3])
    if 'rotating_lasers' in visualization_flags:
        rotating_lasers = ast.literal_eval(file_contents[3])
    if 'wormhole_pairs' in visualization_flags:
        wormhole_pairs = ast.literal_eval(file_contents[4])

    return ProblemConfiguration(
        barriers=barriers,
        static_lasers=static_lasers,
        rotating_lasers=rotating_lasers,
        wormhole_pairs=wormhole_pairs
    )

def extract_solution_configuration(solution_file):
    file_contents = []
    with open(solution_file) as f:
        file_contents = f.readlines()
    file_contents = [line.strip() for line in file_contents]
    return SolutionConfiguration(
        path=ast.literal_eval(file_contents[0])
    )

class ProblemConfiguration:
    def __init__(self, barriers = [], static_lasers = [], rotating_lasers = [], wormhole_pairs = []):
        self.barriers = barriers
        self.static_lasers = static_lasers
        self.rotating_lasers = rotating_lasers
        self.wormhole_pairs = flatten(wormhole_pairs)
        self.bounds = get_bounds(barriers,
                                 [(l[0], l[1]) for l in static_lasers],
                                 [(l[0], l[1]) for l in rotating_lasers],
                                 self.wormhole_pairs)

    def hasBarrierAt(self, x, y):
        return any([b[0] == x and b[1] == y for b in self.barriers])

class SolutionConfiguration:
    def __init__(self, path):
        self.path = path
        self.bounds = get_bounds(path)

    def hasOriginAt(self, x, y):
        return len(self.path) > 0 and self.path[0][0] == x and self.path[0][1] == y

    def hasDestinationAt(self, x, y):
        return len(self.path) > 0 and self.path[-1][0] == x and self.path[-1][1] == y

class Frame:
    def __init__(self, problem_configuration, solution_configuration, buffer = 3):
        self.problem_configuration = problem_configuration
        self.solution_configuration = solution_configuration
        self.path = solution_configuration.path
        self.barriers = set(problem_configuration.barriers)
        self.buffer = buffer
        self.bounds = buffer_bounds(merge_bounds(problem_configuration.bounds, solution_configuration.bounds), buffer)
        base_grid = []
        for y in xrange(self.bounds.y_max, self.bounds.y_min - 1, -1):
            base_grid.append([])
            row = base_grid[-1]
            for x in xrange(self.bounds.x_min, self.bounds.x_max):
                value = ' '
                if problem_configuration.hasBarrierAt(x, y):
                    value = OBSTACLE_CHARACTER
                if solution_configuration.hasOriginAt(x, y):
                    value = ORIGIN_CHARACTER
                if solution_configuration.hasDestinationAt(x, y):
                    value = DESTINATION_CHARACTER

                row.append(value)
        self.base_grid = base_grid

    def display(self, t=0):
        print('Time: {0}'.format(t))
        grid = deepcopy(self.base_grid)

        # Write the wormholes out
        if t % WORMHOLE_FREQUENCY == 0:
            for wormhole in self.problem_configuration.wormhole_pairs:
                self.writeToGrid(grid, WORMHOLE_CHARACTER, wormhole[0], wormhole[1])

        # Write out the locations of the static lasers and their beams
        for laser in self.problem_configuration.static_lasers:
            grid = self.writeOutLaser(grid, laser)

        # Write out the locations of the rotating lasers and their beams
        for laser in self.problem_configuration.rotating_lasers:
            grid = self.writeOutLaser(grid, laser, t)

        # Finally write the location of the robot
        if len(self.path) > 0:
            self.writeToGrid(grid, ROBOT_CHARACTER, self.path[t][0], self.path[t][1])
        for row in grid:
            print(''.join(row))

    def writeToGrid(self, grid, character, x, y):
        grid[self.bounds.y_max - y][x - self.bounds.x_min] = character

    def writeOutLaser(self, grid, laser, t=0):
        dir_x, dir_y = 0, 0
        x_limit, y_limit = -1, -1
        laser_direction_index = LASER_DIRECTIONS.index(laser[2])
        laser_direction = LASER_DIRECTIONS[(laser_direction_index + t) % 4]
        x_limit_predicate, y_limit_predicate = lambda x: True, lambda y: True
        if laser_direction == NORTH:
            dir_x, dir_y = 0, 1
            y_limit_predicate = lambda y: y < self.bounds.y_max
        if laser_direction == EAST:
            dir_x, dir_y = 1, 0
            x_limit_predicate = lambda x: x < self.bounds.x_max
        if laser_direction == SOUTH:
            dir_x, dir_y = 0, -1
            y_limit_predicate = lambda y: y > self.bounds.y_min
        if laser_direction == WEST:
            dir_x, dir_y = -1, 0
            x_limit_predicate = lambda x: x > self.bounds.x_min

        laser_x, laser_y = laser[:2]
        self.writeToGrid(grid, LASER_CHARACTER, laser_x, laser_y)
        beam_x, beam_y = laser_x + dir_x, laser_y + dir_y
        while x_limit_predicate(beam_x) and y_limit_predicate(beam_y):
            if (beam_x, beam_y) in self.barriers:
                break
            self.writeToGrid(grid, LASER_BEAM_CHARACTER, beam_x, beam_y)
            beam_x += dir_x
            beam_y += dir_y
        return grid

def get_bounds(*iterables):
    x_min, y_min = get_lower_bounds(*iterables)
    x_max, y_max = get_upper_bounds(*iterables)

    return Bbox(x_min, y_min, x_max, y_max)

def get_lower_bounds(*iterables):
    x_min, y_min = float('+inf'), float('+inf')
    for x, y in itertools.chain(*iterables):
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
    return x_min, y_min

def get_upper_bounds(*iterables):
    x_max, y_max = float('-inf'), float('-inf')
    for x, y in itertools.chain(*iterables):
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y
    return x_max, y_max

def merge_bounds(*bounds):
    x_min, y_min = get_lower_bounds([(b.x_min, b.y_min) for b in bounds])
    x_max, y_max = get_upper_bounds([(b.x_max, b.y_max) for b in bounds])

    return Bbox(x_min, y_min, x_max, y_max)

    # return get_bounds(flatten([[(b.x_min, b.y_min), (b.x_max, b.y_max)] for b in bounds]))

def buffer_bounds(bounds, buffer=1):
    return Bbox(bounds.x_min - buffer, bounds.y_min - buffer, bounds.x_max + buffer, bounds.y_max + buffer)

def flatten(iterable):
    return [item for sublist in iterable for item in sublist]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_file', help='The input problem text file')
    parser.add_argument('solution_file', help='The output solution text file')
    parser.add_argument('--visualize', nargs='+', help='What flags to visualize', required=False,
                        default=['barriers', 'rotating_lasers', 'wormhole_pairs'])
    args = parser.parse_args()

    for flag in args.visualize:
        if flag not in VISUALIZE_FLAGS:
            raise Exception('{0} is not a recognized argument for visualization'.format(flag))

    if 'static_lasers' in args.visualize and 'rotating_lasers' in args.visualize:
        raise Exception('static_lasers and rotating_lasers cannot both be specified for visualization!')

    pc = extract_problem_configuration(args.problem_file, args.visualize)
    sc = extract_solution_configuration(args.solution_file)

    frame = Frame(pc, sc, buffer=GRID_BUFFER)
    if len(sc.path) == 0:
        frame.display()
        print('No solution provided!')
        sys.exit(0)

    min_time, max_time = 0, len(sc.path) - 1
    current_time = 0
    while True:
        frame.display(current_time)
        input_key = raw_input('Press "n" to advance in time, and "b" to go back, and "q" to exit\n')
        if input_key not in VALID_KEYS:
            print("Invalid input!")
            continue
        if input_key == 'q':
            break
        if input_key == 'n':
            current_time = min(max_time, current_time + 1)
        if input_key == 'b':
            current_time = max(min_time, current_time - 1)
