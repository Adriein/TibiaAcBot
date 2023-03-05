import pyautogui

from .ImageIsNotNumber import ImageIsNotNumber
from .Scanner import Scanner
from .ScreenRegion import ScreenRegion
from FilesystemPackage import File
from LoggerPackage import Logger


class HitPoint:
    def get(self) -> int:
        hit_point_label_location = pyautogui.locateOnScreen(
            'Wiki/Stat/hp_heart.png',
            confidence=0.8,
            grayscale=True,
            region=(1600, 0, 500, 1000)
        )

        number_collection = []
        region = ScreenRegion(
            hit_point_label_location.left + 108,
            hit_point_label_location.top,
            8,
            12
        )

        try:
            while True:
                self.__take_number_screenshot(region)

                result = Scanner.number(confidence=0.6)

                number_collection.append(result)

                self.__clean_number_image()

                region = self.__move_needle(region)
        except ImageIsNotNumber as error:
            Logger.debug(str(error))

            self.__clean_number_image()

            return int(str.join("", map(str, number_collection)))

    def __move_needle(self, region: ScreenRegion) -> ScreenRegion:
        return ScreenRegion(
            region.left + 7,
            region.top,
            region.width + 1,
            region.height
        )

    def __take_number_screenshot(self, region: ScreenRegion):
        """
        pyautogui.screenshot(f'Tmp/{region.left}.png', region=(
            region.left,
            region.top,
            region.width,
            region.height
        ))
        """
        pyautogui.screenshot(f'Tmp/PlayerStatus/{region.left}.png', region=(
            region.left,
            region.top,
            region.width,
            region.height
        ))

    def __clean_number_image(self):
        File.delete_png('Tmp/PlayerStatus')
