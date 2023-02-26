import pyautogui
from ScreenAnalizerPackage import ScreenRegion


class Scanner:
    @staticmethod
    def number(region: ScreenRegion) -> int:
        for number in range(10):
            numberOnScreen = pyautogui.locateOnScreen(
                f'Wiki/Number/${number}.png',
                region=(region.left, region.top, region.width, region.height)
            )

            if numberOnScreen:
                return number
