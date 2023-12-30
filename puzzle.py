from __future__ import annotations

import copy
import itertools
import random

from types_abc import Board


class Puzzle:
    """N*M sliding puzzle"""

    BLANK = 0

    def __init__(self, n_rows: int, n_cols: int, initial_board: Board | None = None) -> None:
        """
        Args:
            n_rows (int): the number of rows (N)
            n_cols (int): the number of columns (M)
            initial_board (Board | None, optional): the initial state of the board.
                If not given, the constructor generate the reachable initial board randomly.
                Defaults to None.
        """
        self.N_ROWS = n_rows
        self.N_COLS = n_cols
        self.board = initial_board if initial_board is not None else self._generate_initial_board()
        self.FINAL_BOARD = [
            [(i * self.N_COLS + j + 1) % (self.N_ROWS * self.N_COLS) for j in range(self.N_COLS)] for i in range(self.N_ROWS)
        ]  # e.g. [[1, 2, 3, 4], [5, 6, 7, 8], ..., [13, 14, 15, 0]]

        if initial_board is not None:
            if not self._is_valid(initial_board):
                raise RuntimeError("The specified board is unreachable.")

    def __str__(self) -> str:
        board_str = ""
        for i in range(self.N_ROWS):
            board_str += "+----" * self.N_COLS + "+\n"
            board_str += "|" + "|".join(f"{num:4}" if num != 0 else " " * 4 for num in self.board[i]) + "|\n"
        board_str += "+----" * self.N_COLS + "+\n"
        return board_str

    def _calculate_parity(self, board_flattened: list[int]) -> int:
        """Calculate the parity of the board.

        Args:
            board_flattened (list[int]): a board flattened to 1-dim array.

        Returns:
            int: the calculated parity.
        """
        inv_count = 0
        for i in range(self.N_ROWS * self.N_COLS):
            for j in range(i + 1, self.N_ROWS * self.N_COLS):
                if board_flattened[i] > board_flattened[j]:
                    inv_count += 1
        perm_parity = inv_count % 2

        return perm_parity

    def _is_valid(self, board: Board) -> bool:
        """Check if the given board is reachable.

        Args:
            board (Board): a board to check

        Returns:
            bool: True if the board is reachable.
        """
        # let numbers be 1-indexed for the calculation of the parity
        # the blank square is signified by N_ROWS * N_COLS
        board_flattened = list(itertools.chain.from_iterable(board))
        idx = board_flattened.index(Puzzle.BLANK)
        board_flattened[idx] = self.N_ROWS * self.N_COLS

        # calculate the parity of the permutation
        perm_parity = self._calculate_parity(board_flattened)

        # calculate the distance of the blank square
        blank_y, blank_x = idx // self.N_COLS, idx % self.N_COLS
        d = abs(self.N_COLS - 1 - blank_x) + abs(self.N_ROWS - 1 - blank_y)
        d_parity = d % 2

        return perm_parity == d_parity

    def _generate_valid_permutation(self) -> list[int]:
        """Generate a reachable permutation

        Returns:
            list[int]: the generated permutation
        """
        # let numbers be 1-indexed for the calculation of the parity
        # the blank square is signified by N_ROWS * N_COLS
        numbers = list(range(1, self.N_ROWS * self.N_COLS + 1))
        while True:
            # generate a permutation randomly
            numbers_shuffled = numbers.copy()
            random.shuffle(numbers_shuffled)

            # calculate the parity of the permutation
            perm_parity = self._calculate_parity(numbers_shuffled)

            # calculate the distance of the blank square
            idx = numbers_shuffled.index(self.N_ROWS * self.N_COLS)
            blank_y, blank_x = idx // self.N_COLS, idx % self.N_COLS
            d = abs(self.N_COLS - blank_x - 1) + abs(self.N_ROWS - blank_y - 1)
            d_parity = d % 2

            if perm_parity == d_parity:  # reachable iff perm_parity == d_parity
                break

        return list(map(lambda x: x if x < self.N_ROWS * self.N_COLS else Puzzle.BLANK, numbers_shuffled))

    def _generate_initial_board(self) -> Board:
        """Generate an initial board randomly which is reachable

        Returns:
            Board: the generated board represented in the N*M list
        """
        perm = self._generate_valid_permutation()

        board = [perm[i : i + self.N_COLS] for i in range(0, self.N_ROWS * self.N_COLS, self.N_COLS)]
        print("initial board generated:")
        print(board)
        return board

    def _convert_num_to_coord(self, n: int) -> tuple[int, int]:
        """convert num to the coordinate in the current board

        Args:
            n (int): the number to search for

        Returns:
            tuple[int, int]: the corresponding coordinate in (row, col) form
        """
        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):
                if self.board[i][j] == n:
                    return i, j

    def _move(self, blank_y: int, blank_x: int, neighbor_y: int, neighbor_x: int) -> Board:
        """swap a square with the blank square
        Args:
            blank_y (int): the y coord of the blank square
            blank_x (int): the x coord of the blank square
            neighbor_y (int): the y coord of the neighbor square
            neighbor_x (int): the x coord of the neighbor square

        Returns:
            Board: the updated board
        """
        board_copied = copy.deepcopy(self.board)
        board_copied[blank_y][blank_x] = board_copied[neighbor_y][neighbor_x]
        board_copied[neighbor_y][neighbor_x] = Puzzle.BLANK
        return board_copied

    def make_moves(self) -> list[Puzzle]:
        """make the list of the possible moves

        Returns:
            list[Puzzle]: the possible moves from the current board
        """
        board_list = []
        blank_y, blank_x = self._convert_num_to_coord(Puzzle.BLANK)

        if blank_y > 0:  # swap with the upper square
            up_y, up_x = blank_y - 1, blank_x
            board_list.append(self._move(blank_y, blank_x, up_y, up_x))

        if blank_y < self.N_ROWS - 1:  # swap with the lower square
            down_y, down_x = blank_y + 1, blank_x
            board_list.append(self._move(blank_y, blank_x, down_y, down_x))

        if blank_x > 0:  # swap with the left square
            left_y, left_x = blank_y, blank_x - 1
            board_list.append(self._move(blank_y, blank_x, left_y, left_x))

        if blank_x < self.N_COLS - 1:  # swap with the right square
            right_y, right_x = blank_y, blank_x + 1
            board_list.append(self._move(blank_y, blank_x, right_y, right_x))

        return list(map(lambda x: Puzzle(self.N_ROWS, self.N_COLS, x), board_list))

    def manhattan_distance(self) -> int:
        """Calculate the sum of the manhattan distance between the current board and the final board

        Returns:
            int: the sum of the distance
        """
        d = 0
        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):
                y, x = self._convert_num_to_coord(self.FINAL_BOARD[i][j])
                d += abs(y - i) + abs(x - j)
        return d
