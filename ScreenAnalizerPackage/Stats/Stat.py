from abc import ABC, abstractmethod
from ScreenAnalizerPackage.ImageIsNotNumber import ImageIsNotNumber
from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Screen import Screen
from .StatNotFound import StatNotFound
from UtilPackage import Array
from FilesystemPackage import File
from LoggerPackage import Logger


class Stat(ABC):
    @abstractmethod
    def find_stat_location(self) -> any:
        pass

    def get(self) -> int:
        stat_location = self.find_stat_location()

        if not stat_location:
            raise StatNotFound

        number_collection = []

        region = ScreenRegion(
            stat_location.left + 129,
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

                region = Screen.move_roi_pointer_left(7, region)

        except ImageIsNotNumber as error:
            Logger.debug(str(error))

            self.__clean_number_image()

            if not number_collection:
                raise StatNotFound

            return int(str.join("", Array.reverse(number_collection)))

    def __take_number_screenshot(self, region: ScreenRegion):
        Screen.roi_screenshot(f'Tmp/{region.left}.png', region)
        Screen.roi_screenshot(f'Tmp/PlayerStatus/{region.left}.png', region)

    def __clean_number_image(self):
        File.delete_png('Tmp/PlayerStatus')
