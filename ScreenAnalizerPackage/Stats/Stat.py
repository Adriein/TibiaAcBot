from abc import ABC, abstractmethod
from ScreenAnalizerPackage.Error.ImageIsNotNumber import ImageIsNotNumber
from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Screen import Screen
from .StatNotFound import StatNotFound
from UtilPackage import Array
import math
import os
import numpy as np
import cv2


class Stat(ABC):
    BASE_STAT_DISTANCE = 117
    BASE_STAT_SEPARATION = 9

    @abstractmethod
    def find_stat_location(self, frame: np.array) -> any:
        pass

    @abstractmethod
    def tmp_folder(self) -> str:
        pass

    def get_stat_roi(self) -> ScreenRegion:
        stats_pixel_width = math.ceil(Screen.MONITOR.width * 20 / 100)
        stats_pixel_height = math.ceil(Screen.MONITOR.height / 2)

        return ScreenRegion(
            start_x=Screen.MONITOR.width - stats_pixel_width,
            end_x=Screen.MONITOR.width,
            start_y=0,
            end_y=stats_pixel_height
        )

    def get(self, frame: np.array) -> int:
        stat_location = self.find_stat_location(frame)

        if not stat_location:
            raise StatNotFound

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        region = ScreenRegion(
            start_x=stat_location.start_x + Stat.BASE_STAT_DISTANCE,
            end_x=stat_location.start_x + Stat.BASE_STAT_DISTANCE + 8,
            start_y=stat_location.start_y,
            end_y=stat_location.start_y + 12,
        )

        number_collection = []

        try:
            while True:
                number_roi = frame[region.start_y: region.end_y, region.start_x: region.end_x]

                result = Scanner.number(confidence=0.6, number_roi=number_roi)

                number_collection.append(result)

                region = Screen.move_roi_pointer_right(7, region)

        except ImageIsNotNumber:
            if not number_collection:
                raise StatNotFound

            return int(str.join("", Array.to_string(number_collection)))

    @staticmethod
    def setup_global_variables() -> None:
        if eval(os.getenv('READ_SAMPLE')):
            Stat.BASE_STAT_DISTANCE = 108
            Stat.BASE_STAT_SEPARATION = 8
