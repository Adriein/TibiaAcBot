import numpy as np
import cv2
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File


class PathFinder:
    def where_am_i(self, frame: np.array):
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        (start_x, end_x, start_y, end_y) = Scanner.mini_map_position(grey_scale_frame)

        mini_map_frame = grey_scale_frame[start_y:end_y, start_x:end_x]

        tibia_map = Cv2File.load_image('Wiki/Ui/Map/Floors/floor-5.png')

        match = cv2.matchTemplate(tibia_map, mini_map_frame, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        test = tibia_map[start_y:100, start_x:100]
        if cv2.waitKey(1):
            cv2.destroyAllWindows()

            # draw the bounding box on the image
        cv2.rectangle(tibia_map, (start_x, start_y), (start_x + 100, start_y + 100), (255, 0, 0), 1)
        # show the output image
        cv2.imshow("Output", test)
        cv2.waitKey(0)
