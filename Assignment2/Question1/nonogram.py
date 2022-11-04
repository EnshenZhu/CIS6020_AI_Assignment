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
        for fileName in os.listdir(folder):
            file_path = os.path.join(folder, fileName)
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

    SolveNonogram(row_value=the_row, column_value=the_column, savepath=output_route)


def find_rest_options(empty_space, groups, ones):
    rest_option_ls = []
    for p in combinations(range(groups + empty_space), groups):
        selected = (groups + empty_space) * [-1]
        ones_idx = 0
        for val in p:
            selected[val] = ones_idx
            ones_idx += 1
        res_opt = [ones[val] + [-1] if val > -1 else [-1] for val in selected]
        res_opt = [item for sublist in res_opt for item in sublist][:-1]
        rest_option_ls.append(res_opt)
    return rest_option_ls


def explore_options(values, no_of_other):
    options = []

    for single_value in values:
        groups = len(single_value)

        not_empty = no_of_other - sum(single_value) - groups + 1
        ones = [[1] * cell for cell in single_value]
        raw_results = find_rest_options(not_empty, groups, ones)
        options.append(raw_results)

    return options


def get_only_one_option(values):
    return [(n, np.unique(idx)[0]) for n, idx in enumerate(np.array(values).T) if len(np.unique(idx)) == 1]


def delete_conflict_options(all_options, idx, value_ls):
    return [option_ls for option_ls in all_options if option_ls[idx] == value_ls]


class SolveNonogram:
    def __init__(self,
                 row_value=[],
                 column_value=[],
                 savepath=''):

        # handle the row profile

        self.row_profile = row_value
        self.row_num = len(row_value)
        self.rows_options = None  # record all the possible options to fill out a row
        self.min_rows = None  # record the minimum possible row expansion
        self.rows_changed = self.row_num * [0]
        self.rows_finished = self.row_num * [0]

        # handle the column profile
        self.column_profile = column_value
        self.column_num = len(column_value)
        self.columns_options = None
        self.min_columns = None
        self.columns_changed = self.column_num * [0]
        self.column_finished = self.column_num * [0]

        self.sorted_options = None
        self.isSolved = False
        self.shape = (self.row_num, self.column_num)
        self.board = [[0 for c in range(self.column_num)] for r in range(self.row_num)]
        self.save_path = savepath

        if self.save_path != '':
            self.teration_idx = 0

        self.solving_work()

    def select_index_not_done(self, options, row_idx):

        num_of_selections = []

        for item in options:
            num_of_selections.append(len(item))

        if row_idx:
            return [(idx, n, row_idx) for idx, n in enumerate(num_of_selections) if self.rows_finished[idx] == 0]
        else:
            return [(i, n, row_idx) for i, n in enumerate(num_of_selections) if self.column_finished[i] == 0]

    def display_board(self):
        plt.imshow(self.board, cmap='Greys')
        plt.axis('off')
        plt.show()

    def save_board(self, increase_size=20):
        name = f'0000000{str(self.teration_idx)}'[-8:]
        increased_board = np.zeros(np.array((self.row_num, self.column_num)) * increase_size)
        for j in range(self.row_num):
            for k in range(self.column_num):
                increased_board[j * increase_size: (j + 1) * increase_size,
                k * increase_size: (k + 1) * increase_size] = self.board[j][k]
        plt.imsave(os.path.join(self.save_path, f'{name}.jpeg'), increased_board, cmap='Greys', dpi=1000)

    def check_done(self, row_idx, idx):
        if row_idx:
            return self.rows_finished[idx]
        else:
            return self.column_finished[idx]

    def should_terminate(self):
        if 0 not in self.rows_finished and 0 not in self.column_finished:
            self.isSolved = True

    def update_finished(self, row_idx, idx):
        if row_idx:
            registry_value = self.board[idx]
        else:
            registry_value = [row[idx] for row in self.board]
        if 0 not in registry_value:
            if row_idx:
                self.rows_finished[idx] = 1
            else:
                self.column_finished[idx] = 1

    def solving_work(self):

        # Explore all the possible options with the given rows and column profile
        self.rows_options = explore_options(self.row_profile, self.column_num)
        self.columns_options = explore_options(self.column_profile, self.row_num)

        start_time = time.time()  # mark the start time
        while not self.isSolved:

            self.min_rows = self.select_index_not_done(self.rows_options, 1)
            self.min_columns = self.select_index_not_done(self.columns_options, 0)
            self.sorted_options = sorted(self.min_rows + self.min_columns, key=lambda element: element[1])

            for temp_idx, dummy_factor, row_idx_series in self.sorted_options:
                if not self.check_done(row_idx_series, temp_idx):
                    if row_idx_series:
                        values = self.rows_options[temp_idx]
                    else:
                        values = self.columns_options[temp_idx]
                    same_ind = get_only_one_option(values)
                    for ind2, temp_value in same_ind:
                        if row_idx_series:
                            a_row_idx, a_column_idx = temp_idx, ind2
                        else:
                            a_row_idx, a_column_idx = ind2, temp_idx
                        if self.board[a_row_idx][a_column_idx] == 0:
                            self.board[a_row_idx][a_column_idx] = temp_value
                            if row_idx_series:
                                self.columns_options[a_column_idx] = delete_conflict_options(
                                    self.columns_options[a_column_idx], a_row_idx,
                                    temp_value)
                            else:
                                self.rows_options[a_row_idx] = delete_conflict_options(self.rows_options[a_row_idx],
                                                                                       a_column_idx,
                                                                                       temp_value)
                            clear_output(wait=True)
                            if self.save_path != '':
                                self.save_board()
                                self.teration_idx += 1
                    self.update_finished(row_idx_series, temp_idx)

            # identify if we should terminate the exploring
            self.should_terminate()

        end_time = time.time()  # mark the end time
        print("This example takes %.4f second to be finished."
              % (end_time - start_time))

        self.display_board()


if __name__ == "__main__":
    filename = sys.argv[1]
    to_solve(example=filename, output_route="outputs/" + filename)
