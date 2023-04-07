from ConsolePackage import Console
from ScreenAnalizerPackage import Screen
from ScreenAnalizerPackage import Coordinate


class Mouse:
    @staticmethod
    def use_left_button(coordinate: Coordinate) -> None:
        (x, y) = coordinate

        Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {x} {y}')
        Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
