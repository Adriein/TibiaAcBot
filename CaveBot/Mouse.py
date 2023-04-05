from ConsolePackage import Console
from ScreenAnalizerPackage import Screen


class Mouse:
    @staticmethod
    def use_left_button(coordinates: tuple[int, int]) -> None:
        (x, y) = coordinates

        Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {x} {y}')
        Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
