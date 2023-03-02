import pyautogui
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

            if number_position_on_screen:
                region = ScreenRegion.from_box(number_position_on_screen)
                print(number)
                return region, number

        return None
