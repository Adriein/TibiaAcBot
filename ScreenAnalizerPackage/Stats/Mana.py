import pyautogui
from ScreenAnalizerPackage.Stats.Stat import Stat


class Mana(Stat):
    def find_stat_location(self) -> any:
        return pyautogui.locateOnScreen(
            'Wiki/Stat/mana.png',
            confidence=0.8,
            grayscale=True,
            region=(1600, 0, 500, 1000)
        )
