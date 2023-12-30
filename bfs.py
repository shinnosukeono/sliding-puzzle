from collections import deque

from puzzle import Puzzle
from types_abc import Algorithm, Board


class BFS(Algorithm):
    """Solve the sliding puzzle in the breadth first search method"""

    def __init__(self) -> None:
        self.n_opened = 0

    def solve(self, puzzle: Puzzle) -> list[Puzzle]:
        """Solve the puzzle

        Args:
            puzzle (Puzzle): the puzzle to solve

        Returns:
            list[Puzzle]: the history of the movements from the start to the final board
        """
        queue: list[list[Puzzle]] = deque([[puzzle]])
        opened_boards_list: list[Board] = []
        current_history: list[Puzzle] = []

        while len(queue) > 0:
            current_history = queue.popleft()
            current_puzzle = current_history[-1]

            # completion judgement
            if current_puzzle.board == puzzle.FINAL_BOARD:
                break

            # not visit again an opened board
            if current_puzzle.board in opened_boards_list:
                continue

            # open current_puzzle
            opened_boards_list.append(current_puzzle.board)
            self.n_opened += 1
            for move in current_puzzle.make_moves():
                if move.board not in opened_boards_list:
                    queue.append(current_history + [move])

        return current_history
