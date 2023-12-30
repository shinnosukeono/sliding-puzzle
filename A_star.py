import copy
import heapq
from functools import total_ordering

from puzzle import Puzzle
from types_abc import Algorithm, Board


@total_ordering
class History:
    """Representing a history of moves and the corresponding heuristics score"""

    def __init__(self, history: list[Puzzle], cost: int, heuristics: str) -> None:
        self.history = history
        self.cost = cost
        self.heuristics = heuristics

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, History):
            return NotImplemented
        return self.cost == __value.cost

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, History):
            return NotImplemented
        return self.cost < __value.cost

    def __getitem__(self, i: int) -> Puzzle:
        return self.history[i]

    def append(self, puzzle: Puzzle) -> None:
        self.cost += getattr(puzzle, self.heuristics)() - getattr(self[-1], self.heuristics)()
        self.history.append(puzzle)


class AStar(Algorithm):
    """Solve the sliding puzzle in the A* method"""

    def __init__(self, heuristics: str) -> None:
        self.n_opened = 0
        self.heuristics = heuristics

    def solve(self, puzzle: Puzzle) -> list[Puzzle]:
        queue: list[History] = [History([puzzle], getattr(puzzle, self.heuristics)(), self.heuristics)]
        current_history: History = None
        opened_boards_list: list[Board] = []

        while len(queue) > 0:
            current_history = heapq.heappop(queue)
            current_puzzle: Puzzle = current_history[-1]

            # completion judgement
            if current_puzzle.board == puzzle.FINAL_BOARD:
                break

            # not visit again an opened board
            if current_puzzle.board in opened_boards_list:
                continue

            # open the current_puzzle
            opened_boards_list.append(current_puzzle.board)
            self.n_opened += 1
            for move in current_puzzle.make_moves():
                if move.board not in opened_boards_list:
                    current_history_copied = History(
                        copy.deepcopy(current_history.history), current_history.cost, self.heuristics
                    )
                    current_history_copied.append(move)
                    heapq.heappush(queue, current_history_copied)

        return current_history.history
