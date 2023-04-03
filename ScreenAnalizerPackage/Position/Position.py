from ScreenAnalizerPackage.Shared.Screen import Screen
from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage import PositionError
import cv2


class Position:
    @staticmethod
    def create() -> 'Position':
        try:
            actual_position = Screen.screenshot()

            (start_x, start_y, end_x, end_y, direction) = Scanner.player_position(
                screenshot=actual_position,
                confidence=0.9
            )

            return Position(start_x, start_y, end_x, end_y, direction)
        except Exception as exception:
            raise PositionError(str(exception))

    def __init__(self, start_x, start_y, end_x, end_y, direction: str):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.direction = direction
