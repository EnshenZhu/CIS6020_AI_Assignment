import os.path
import time

from NonogramSolver import NonogramSolver
from Question1.empty_the_folder import to_empty

all_example_ls = {
    "example1": [
        [[3], [3], [1, 1], [3], [1, 1]],
        [[3], [1], [2, 2], [2], [3]]
    ],
    "example2": [
        [[2], [2], [2], [2, 2], [3]],
        [[2], [3], [1], [2, 2], [2, 1]]
    ],
    "example3": [
        [[2], [2, 1], [1, 1], [3], [1, 1], [1, 1], [2], [1, 1], [1, 2], [2]],
        [[2, 1], [2, 1, 3], [7], [1, 3], [2, 1]]
    ],
    "example4": [
        [[1, 2], [2], [1], [1], [2], [2, 4], [2, 6], [8], [1, 1], [2, 2]],
        [[2], [3], [1], [2, 1], [5], [4], [1, 4, 1], [1, 5], [2, 2], [2, 1]]
    ],
    "example5": [
        [[3], [5], [3, 1], [2, 1], [3, 3, 4], [2, 2, 7], [6, 1, 1], [4, 2, 2], [1, 1], [3, 1], [6], [2, 7], [6, 3, 1],
         [1, 2, 2, 1, 1], [4, 1, 1, 3], [4, 2, 2], [3, 3, 1], [3, 3], [3], [2, 1]],
        [[2], [1, 2], [2, 3], [2, 3], [3, 1, 1], [2, 1, 1], [1, 1, 1, 2, 2], [1, 1, 3, 1, 3], [2, 6, 4], [3, 3, 9, 1],
         [5, 3, 2], [3, 1, 2, 2], [2, 1, 7], [3, 3, 2], [2, 4], [2, 1, 2], [2, 2, 1], [2, 2], [1], [1]]
    ]
}


def to_solve(example, output_route):
    # empty the target directory firstly
    to_empty(os.path.join("./output/", example))

    ls = all_example_ls[example]
    the_row = ls[0]  # extract the row list
    the_column = ls[1]  # extract the column list

    start_time = time.time()
    NonogramSolver(ROWS_VALUES=the_row, COLS_VALUES=the_column, savepath=output_route)
    end_time = time.time()
    print("Finish on the %s; It requires %d iterations, and take %.4f second to be finished."
          % (example, len(the_row) * len(the_column), end_time - start_time))


if __name__ == "__main__":
    # to_solve(example="example1", output_route="output/example1")
    # to_solve(example="example2", output_route="output/example2")
    # to_solve(example="example3", output_route="output/example3")
    # to_solve(example="example4", output_route="output/example4")
    to_solve(example="example5", output_route="output/example5")
