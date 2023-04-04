from ConsolePackage.Console import Console
from ScreenAnalizerPackage.Shared.Screen import Screen


class Keyboard:
    @staticmethod
    def press(key: str):
        Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
