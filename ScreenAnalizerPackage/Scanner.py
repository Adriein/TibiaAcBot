import pyautogui
import cv2
from .ScreenRegion import ScreenRegion


class Scanner:
    @staticmethod
    def number(region: ScreenRegion) -> tuple[ScreenRegion, int] | None:
        for number in range(10):
            number_position_on_screen = pyautogui.locateOnScreen(
                f'Wiki/Number/{number}.png',
                grayscale=True,
                confidence=0.7,
                region=(region.left, region.top, region.width, region.height)
            )

            match = cv2.matchTemplate(f'Wiki/Number/{number}.png', '/Tmp/1797.png', cv2.TM_CCOEFF_NORMED)
            res = cv2.minMaxLoc(match)
            matchConfidence = res[1]

            if number_position_on_screen:
                region = ScreenRegion.from_box(number_position_on_screen)
                print(number)
                return region, number

        return None
