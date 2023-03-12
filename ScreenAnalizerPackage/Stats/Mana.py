import pyautogui
from ScreenAnalizerPackage.Stats.Stat import Stat


class Mana(Stat):
    def find_stat_location(self) -> any:
        [left, top, width, height] = self.get_stat_roi()
        return pyautogui.locateOnScreen(
            'Wiki/Stat/mana.png',
            confidence=0.8,
            grayscale=True,
            region=(left, top, width, height)
        )
