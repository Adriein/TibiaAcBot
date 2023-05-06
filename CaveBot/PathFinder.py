import numpy as np
import cv2
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File
from .MapCoordinate import MapCoordinate
from ScreenAnalizerPackage import Coordinate


class PathFinder:
    def where_am_i(self, frame: np.array):
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        (start_x, end_x, start_y, end_y) = Scanner.mini_map_position(grey_scale_frame)

        mini_map_frame = grey_scale_frame[start_y:end_y, start_x:end_x]

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-5.png')

        match = cv2.matchTemplate(tibia_map, mini_map_frame, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        test = tibia_map[start_y - 100:start_y + 100, start_x - 100:start_x + 100]

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

        # show the output image
        cv2.imshow("Output", test)
        cv2.waitKey(0)

        # print(max_coordinates)
        # print(max_coincidence)

    def __get_pixel_from_coordinate(self, coordinate: MapCoordinate) -> Coordinate:
        return Coordinate(coordinate.x - 31744, coordinate.y - 30976)

    def map_position_based_on_map_coordinate(self) -> None:
        map_coordinate = MapCoordinate(32063, 31884, 5)

        coordinate = self.__get_pixel_from_coordinate(map_coordinate)

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-{map_coordinate.z}.png')

        cv2.drawMarker(tibia_map, (coordinate.x, coordinate.y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)

        test = tibia_map[coordinate.y - 100:coordinate.y + 100, coordinate.x - 100:coordinate.x + 100]

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

        # show the output image
        cv2.imshow("Output", test)
        cv2.waitKey(0)