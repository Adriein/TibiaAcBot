from ConsolePackage import Console
from ScreenAnalizerPackage import Screen
from ScreenAnalizerPackage import Coordinate


class Mouse:
    @staticmethod
    def use_left_button(coordinate: Coordinate) -> None:
        Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {coordinate.x} {coordinate.y}')
        Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
