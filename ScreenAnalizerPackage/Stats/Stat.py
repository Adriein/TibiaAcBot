from abc import ABC, abstractmethod
from ScreenAnalizerPackage.ImageIsNotNumber import ImageIsNotNumber
from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Screen import Screen
from .StatNotFound import StatNotFound
from UtilPackage import Array
from FilesystemPackage import File
from LoggerPackage import Logger
import math
import os


class Stat(ABC):
    BASE_STAT_DISTANCE = 116
    @abstractmethod
    def find_stat_location(self) -> any:
        pass

    def get_stat_roi(self) -> ScreenRegion:
        stats_pixel_width = math.ceil(Screen.MONITOR.width * 20 / 100)
        stats_pixel_height = math.ceil(Screen.MONITOR.height / 2)

        return ScreenRegion(
            left=Screen.MONITOR.width - stats_pixel_width,
            top=0,
            width=stats_pixel_width,
            height=stats_pixel_height
        )

    def get(self) -> int:
        stat_location = self.find_stat_location()

        if not stat_location:
            raise StatNotFound

        number_collection = []

        region = ScreenRegion(
            stat_location.left + Stat.BASE_STAT_DISTANCE,
            stat_location.top,
            8,
            12
        )

        try:
            while True:
                self.__take_number_screenshot(region)

                result = Scanner.number(confidence=0.6)

                number_collection.append(result)

                self.__clean_number_image()

                region = Screen.move_roi_pointer_right(7, region)

        except ImageIsNotNumber as error:
            Logger.debug(str(error))

            self.__clean_number_image()

            if not number_collection:
                raise StatNotFound

            return int(str.join("", Array.to_string(number_collection)))

    def __take_number_screenshot(self, region: ScreenRegion):
        Screen.roi_screenshot(f'Tmp/{region.left}.png', region)
        Screen.roi_screenshot(f'Tmp/PlayerStatus/{region.left}.png', region)

    def __clean_number_image(self):
        File.delete_png('Tmp/PlayerStatus')

    @staticmethod
    def setup_global_variables() -> None:
        if eval(os.getenv('READ_SAMPLE')):
            Stat.BASE_STAT_DISTANCE = 108
