from ConsolePackage import Console
from ScreenAnalizerPackage import Screen


class Mouse:
    @staticmethod
    def use_left_button(coordinates: tuple[int, int]) -> None:
        (x, y) = coordinates
        print(Screen.TIBIA_WINDOW_ID)
        print(x)
        print(y)
        Console.execute(f'xdotool windowmove --sync {Screen.TIBIA_WINDOW_ID} {x} {y} click 1')
