from ScreenAnalizerPackage.Stats.Stat import Stat
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class HitPoint(Stat):
    TMP_FOLDER = 'hp'

    def tmp_folder(self) -> str:
        return self.TMP_FOLDER

    def find_stat_location(self, frame: np.array) -> ScreenRegion:
        region = self.get_stat_roi()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hp_roi = frame[region.start_y: region.end_y, region.start_x: region.end_x]

        hp_stat_template = Cv2File.load_image('Wiki/Stat/hp.png')

        match = cv2.matchTemplate(hp_roi, hp_stat_template, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        height, width = hp_stat_template.shape

        frame_start_x = region.start_x + start_x
        frame_start_y = region.start_y + start_y
        frame_end_x = frame_start_x + width
        frame_end_y = frame_start_y + height

        return ScreenRegion(start_x=frame_start_x, end_x=frame_end_x, start_y=frame_start_y, end_y=frame_end_y)
