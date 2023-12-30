from typing import Type

from A_star import AStar
from bfs import BFS
from puzzle import Puzzle
from types_abc import Algorithm, Board


class SlidingPuzzleSolver:
    def __init__(self, n_rows: int, n_cols: int, initial_board: Board | None = None) -> None:
        self.puzzle = Puzzle(n_rows, n_cols, initial_board)

    def run(self, method: Type[Algorithm], heuristics: str | None = None) -> None:
        if method is BFS:
            algorithm = BFS()
        elif method is AStar:
            algorithm = AStar(heuristics)

        history = algorithm.solve(self.puzzle)
        print("The puzzle is solved.")
        print(f"The number of the searched boards: {algorithm.n_opened}")
        for i, board in enumerate(history):
            print(f"Step {i}:")
            print(board)
