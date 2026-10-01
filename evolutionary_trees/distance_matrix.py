#!/usr/bin/env python3
from dataclasses import dataclass
from pprint import pprint

@dataclass
class DistanceMatrix:
    matrix: list[list[float]]

    def add_row_col(self, row: int, col: int, cluster_size_1: int, cluster_size_2: int):
        new_row = [0.0] * (len(self.matrix) + 1)
        for r in range(len(new_row) - 1):
            new_dist = (self.matrix[row][r] * cluster_size_1 + self.matrix[r][col] * cluster_size_2) / (
                cluster_size_1 + cluster_size_2
            )
            new_row[r] = new_dist
        for row, item in zip(self.matrix, new_row):
            row.append(item)
        self.matrix.append(new_row.copy())

    def del_rows_cols(self, indices: list[int]):
        sorted_indices = sorted(indices, reverse=True)
        for index in sorted_indices:
            del self.matrix[index]
        for index in sorted_indices:
            for row in self.matrix:
                del row[index]

    def find_min_element(self) -> tuple[int, int, float]:
        curr_min = self.matrix[0][1]
        curr_row = 0
        curr_col = 1
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j, item in enumerate(row):
                if i == j:
                    continue
                if item < curr_min and item != 0:
                    curr_min = item
                    curr_row = i
                    curr_col = j
        return curr_row, curr_col, curr_min

def load(path) -> tuple[DistanceMatrix, list[str]]:
    labels = []
    matrix = []
    with open(path) as f:
        for line in f:
            row = []
            pieces = line.strip().split(',')
            labels.append(pieces[0])
            row.extend(float(p) for p in pieces[1:])
            matrix.append(row)
    return DistanceMatrix(matrix), labels

def test_find_min_element():
    # load test data
    # or define in function; that's fine too for now
    d = DistanceMatrix(
        matrix=[
            [0, 3, 4, 3],
            [3, 0, 4, 5],
            [4, 4, 0, 2],
            [3, 5, 2, 0],
        ]
    )

    print(d.find_min_element())
    assert d.find_min_element() == (2, 3, 2)

def test_add_row_col():
    d = DistanceMatrix(
        matrix=[
            [0, 3, 4, 3],
            [3, 0, 4, 5],
            [4, 4, 0, 2],
            [3, 5, 2, 0],
        ]
    )

    #print(d)
    pprint(d.matrix)
    d.add_row_col(2, 3, 1, 2)
    pprint(d.matrix)

    assert d.matrix == [
        [0, 3, 4, 3, 3.5],
        [3, 0, 4, 5, 4.5],
        [4, 4, 0, 2, 0],
        [3, 5, 2, 0, 0],
        [3.5, 4.5, 0, 0, 0],
    ]

def test_del_rows_cols():
    d = DistanceMatrix(
            matrix=[
            [0, 3, 4, 3, 3.5],
            [3, 0, 4, 5, 4.5],
            [4, 4, 0, 2, 0],
            [3, 5, 2, 0, 0],
            [3.5, 4.5, 0, 0, 0],
        ]
    )

    d.del_rows_cols([2, 3])
    pprint(d.matrix)

    assert d.matrix == [
        [0, 3, 3.5],
        [3, 0, 4.5],
        [3.5, 4.5, 0],
    ]
