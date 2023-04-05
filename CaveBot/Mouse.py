from ConsolePackage import Console
from ScreenAnalizerPackage import Screen


class Mouse:
    @staticmethod
    def use_left_button(coordinates: tuple[int, int]) -> None:
        (x, y) = coordinates
        Console.execute(f'xdotool windowmove --sync --window {Screen.TIBIA_WINDOW_ID} {x} {y} click 1')
