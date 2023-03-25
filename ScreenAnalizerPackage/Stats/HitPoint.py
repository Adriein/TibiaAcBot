import pyautogui
from ScreenAnalizerPackage.Stats.Stat import Stat


class HitPoint(Stat):
    TMP_FOLDER = 'hp'

    def tmp_folder(self) -> str:
        return self.TMP_FOLDER

    def find_stat_location(self) -> any:
        region = self.get_stat_roi()

        return pyautogui.locateOnScreen(
            'Wiki/Stat/hp.png',
            confidence=0.8,
            grayscale=True,
            region=(region.left, region.top, region.width, region.height)
        )
