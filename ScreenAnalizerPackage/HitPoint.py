import pyautogui
from .Scanner import Scanner
from .ScreenRegion import ScreenRegion


class HitPoint:
    def get(self) -> int:
        hit_point_label_location = pyautogui.locateOnScreen(
            'Wiki/Stat/hp_heart.png',
            confidence=0.8,
            grayscale=True,
            region=(1600, 0, 500, 1000)
        )

        print(hit_point_label_location)
        number_collection = []
        region = ScreenRegion(
            hit_point_label_location.left + 108,
            hit_point_label_location.top,
            8,
            12
        )

        for number in range(3):
            print(region.left)
            result = Scanner.number(region)

            if not result:
                break

            number_collection.append(result)
            region = self.__move_needle(result[0])

        raise Exception
        """
        for number in range(3):
            result = Scanner.number(region)

            if not result:
                break

            number_collection.append(result)
            region = self.__move_needle(result[0])
            
        
                hit_points = pyautogui.screenshot(f'Tmp/screenshot.png', region=(
            hit_point_label_location.left + 108,
            hit_point_label_location.top,
            8,
            12
        ))
        """
        return 0

    def __move_needle(self, region: ScreenRegion) -> ScreenRegion:
        pyautogui.screenshot(f'Tmp/{region.left}.png', region=(
            region.left + 7,
            region.top,
            region.width + 2,
            region.height
        ))
        return ScreenRegion(
            region.left + 7,
            region.top,
            region.width + 2,
            region.height
        )
