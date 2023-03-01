import pyautogui
from ScreenAnalizerPackage import ScreenRegion


class Scanner:
    @staticmethod
    def number(region: ScreenRegion) -> dict[int, int]:
        numberYPositionDictonary = {}

        for number in range(10):
            numberPositionOnScreen = pyautogui.locateOnScreen(
                f'Wiki/Number/{number}.png',
                confidence=0.8,
                grayscale=True,
                region=(region.left, region.top, region.width, region.height)
            )
            print(numberPositionOnScreen)
            if numberPositionOnScreen:
                numberYPositionDictonary[numberPositionOnScreen.left] = number

        return numberYPositionDictonary