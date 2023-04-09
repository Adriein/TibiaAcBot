from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage import PositionError
import numpy as np


class Position:
    @staticmethod
    def check(frame: np.array) -> 'Position':
        try:
            (start_x, start_y, end_x, end_y, direction) = Scanner.player_position(frame, confidence=0.8)

            return Position(start_x, start_y, end_x, end_y, direction)
        except Exception as exception:
            raise PositionError(str(exception))

    def __init__(self, start_x, start_y, end_x, end_y, direction: str):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.direction = direction
