import sys
import time
from itertools import combinations
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

protected_folder_location_list = [
    '../.idea',
    '../venv',
    '../input_assets',
    '../forbid'
]

all_example_ls = {
    # 5 * 5
    "example1": [
        [[3], [3], [1, 1], [3], [1, 1]],
        [[3], [1], [2, 2], [2], [3]]
    ],

    # 5 * 5
    "example2": [
        [[2], [2], [2], [2, 2], [3]],
        [[2], [3], [1], [2, 2], [2, 1]]
    ],

    # 10 * 5
    "example3": [
        [[2], [2, 1], [1, 1], [3], [1, 1], [1, 1], [2], [1, 1], [1, 2], [2]],
        [[2, 1], [2, 1, 3], [7], [1, 3], [2, 1]]
    ],

    # 10 * 10
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


class solveNonogram:
    def __init__(self,
                 row_profile=[],
                 column_profile=[],
                 savepath=''):

        # handle the row profile
        self.row_profile = row_profile
        self.row_length = len(row_profile)
        self.rows_changed = self.row_length * [0]
        self.rows_done = self.row_length * [0]

        # handle the column profile
        self.COLS_VALUES = column_profile
        self.num_of_columns = len(column_profile)
        self.cols_changed = self.num_of_columns * [0]
        self.cols_done = self.num_of_columns * [0]

        self.solved = False
        self.shape = (self.row_length, self.num_of_columns)
        self.board = [[0 for c in range(self.num_of_columns)] for r in range(self.row_length)]
        self.save_path = savepath

        # step 1: Defining all possible solutions for every row and col
        self.rows_possibilities = self.create_possibilities(row_profile, self.num_of_columns)
        self.cols_possibilities = self.create_possibilities(column_profile, self.row_length)

        start_time = time.time()  # mark the start time
        while self.solved == False:

            # step 2: Order indici by lowest
            self.lowest_rows = self.select_index_not_done(self.rows_possibilities, 1)
            self.lowest_cols = self.select_index_not_done(self.cols_possibilities, 0)
            self.lowest = sorted(self.lowest_rows + self.lowest_cols, key=lambda element: element[1])

            # step 3: Get only zeroes or only ones of the lowest possibility
            for ind1, _, row_ind in self.lowest:
                if not self.check_done(row_ind, ind1):
                    if row_ind:
                        values = self.rows_possibilities[ind1]
                    else:
                        values = self.cols_possibilities[ind1]
                    same_ind = self.get_only_one_option(values)
                    for ind2, val in same_ind:
                        if row_ind:
                            ri, ci = ind1, ind2
                        else:
                            ri, ci = ind2, ind1
                        if self.board[ri][ci] == 0:
                            self.board[ri][ci] = val
                            if row_ind:
                                self.cols_possibilities[ci] = self.remove_possibilities(self.cols_possibilities[ci], ri,
                                                                                        val)
                            else:
                                self.rows_possibilities[ri] = self.remove_possibilities(self.rows_possibilities[ri], ci,
                                                                                        val)
                            clear_output(wait=True)
                            # self.display_board()
                            if self.save_path != '':
                                self.save_board()
                                self.n += 1
                    self.update_done(row_ind, ind1)
            self.check_solved()

        end_time = time.time()  # mark the end time
        print("This example takes %.4f second to be finished."
              % (end_time - start_time))

        self.display_board()

    def create_possibilities(self, values, no_of_other):
        possibilities = []

        for v in values:
            groups = len(v)
            no_empty = no_of_other - sum(v) - groups + 1
            ones = [[1] * x for x in v]
            res = self._create_possibilities(no_empty, groups, ones)
            possibilities.append(res)

        return possibilities

    def _create_possibilities(self, n_empty, groups, ones):
        res_opts = []
        for p in combinations(range(groups + n_empty), groups):
            selected = [-1] * (groups + n_empty)
            ones_idx = 0
            for val in p:
                selected[val] = ones_idx
                ones_idx += 1
            res_opt = [ones[val] + [-1] if val > -1 else [-1] for val in selected]
            res_opt = [item for sublist in res_opt for item in sublist][:-1]
            res_opts.append(res_opt)
        return res_opts

    def select_index_not_done(self, possibilities, row_ind):
        s = [len(i) for i in possibilities]
        if row_ind:
            return [(i, n, row_ind) for i, n in enumerate(s) if self.rows_done[i] == 0]
        else:
            return [(i, n, row_ind) for i, n in enumerate(s) if self.cols_done[i] == 0]

    def get_only_one_option(self, values):
        return [(n, np.unique(i)[0]) for n, i in enumerate(np.array(values).T) if len(np.unique(i)) == 1]

    def remove_possibilities(self, possibilities, i, val):
        return [p for p in possibilities if p[i] == val]

    def display_board(self):
        plt.imshow(self.board, cmap='Greys')
        plt.axis('off')
        plt.show()

    def save_board(self, increase_size=20):
        name = f'0000000{str(self.n)}'[-8:]
        increased_board = np.zeros(np.array((self.row_length, self.num_of_columns)) * increase_size)
        for j in range(self.row_length):
            for k in range(self.num_of_columns):
                increased_board[j * increase_size: (j + 1) * increase_size,
                k * increase_size: (k + 1) * increase_size] = self.board[j][k]
        plt.imsave(os.path.join(self.save_path, f'{name}.jpeg'), increased_board, cmap='Greys', dpi=1000)

    def update_done(self, row_ind, idx):
        if row_ind:
            vals = self.board[idx]
        else:
            vals = [row[idx] for row in self.board]
        if 0 not in vals:
            if row_ind:
                self.rows_done[idx] = 1
            else:
                self.cols_done[idx] = 1

    def check_done(self, row_ind, idx):
        if row_ind:
            return self.rows_done[idx]
        else:
            return self.cols_done[idx]

    def check_solved(self):
        if 0 not in self.rows_done and 0 not in self.cols_done:
            self.solved = True


def is_protected(test_folder_location):
    if test_folder_location in protected_folder_location_list:
        return True
    else:
        return False


def to_empty(folder_location):
    folder = folder_location

    # identify if the target folder is protected, which should not be emptied
    if is_protected(test_folder_location=folder):
        print('%s folder should not be emptied' % folder)
        return
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def to_solve(example, output_route):
    # empty the target directory firstly
    to_empty(os.path.join("outputs/", example))

    ls = all_example_ls[example]
    the_row = ls[0]  # extract the row list
    the_column = ls[1]  # extract the column list

    solveNonogram(row_profile=the_row, column_profile=the_column, savepath=output_route)


if __name__ == "__main__":
    filename = sys.argv[1]
    to_solve(example=filename, output_route="outputs/" + filename)
