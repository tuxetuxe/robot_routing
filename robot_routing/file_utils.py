import ast
from world import World


def read_world_from_problem_file(problem_file):
    file_contents = []

    with open(problem_file) as f:
        file_contents = f.readlines()

    file_contents = [line.strip() for line in file_contents]

    origin = ast.literal_eval(file_contents[0])
    destination = ast.literal_eval(file_contents[1])
    barriers = ast.literal_eval(file_contents[2])
    lasers = ast.literal_eval(file_contents[3])
    wormhole_pairs = ast.literal_eval(file_contents[4])

    return World(
        origin=origin,
        destination=destination,
        barriers=barriers,
        lasers=lasers,
        wormhole_pairs=wormhole_pairs
    )


def write_solution_file(solution_file, solution_path):
    with open(solution_file, 'w') as file:
        file.write("%s" % solution_path)
