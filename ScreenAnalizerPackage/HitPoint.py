import pyautogui
from .Scanner import Scanner
from .ScreenRegion import ScreenRegion


class HitPoint:
    def get(self) -> int:
        hit_point_label_location = pyautogui.locateOnScreen(
            'Wiki/Stat/hp.png',
            confidence=0.8,
            grayscale=True,
            region=(1549, 74, 500, 1000)
        )

        number_collection = []
        region = ScreenRegion(
                    hit_point_label_location.left + 65,
                    hit_point_label_location.top,
                    53,
                    20
                )

        for number in range(3):
            print(region.left)
            result = Scanner.number(region)

            if not result:
                break

            number_collection.append(result)
            region = self.__move_needle(result[0])

        return 0

    def __move_needle(self, region: ScreenRegion) -> ScreenRegion:
        pyautogui.screenshot(f'Wiki/{region.left}.png')
        return ScreenRegion(
            region.left + 10,
            region.top,
            region.width,
            region.height
        )
