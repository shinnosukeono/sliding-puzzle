from abc import ABC, abstractmethod
from enum import Enum
from typing import List

Board = List[List[int]]


class Algorithm(ABC):
    n_opened = 0

    @abstractmethod
    def solve(self, puzzle) -> list:
        return NotImplemented


class Location(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Direction(Enum):
    UP = 0
    UPPER_LEFT = 1
    LEFT = 2
    LOWER_LEFT = 3
    DOWN = 4
    LOWER_RIGHT = 5
    RIGHT = 6
    UPPER_RIGHT = 7
