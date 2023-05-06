import numpy as np
import cv2
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File
from .MapCoordinate import MapCoordinate
from ScreenAnalizerPackage import Coordinate
from ScreenAnalizerPackage import ScreenRegion


class PathFinder:
    def where_am_i(self, frame: np.array):
        initial_map_coordinate = MapCoordinate(32063, 31884, 5)
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-5.png')

        # find position of minimap in the screen

        (start_x, end_x, start_y, end_y) = Scanner.mini_map_position(grey_scale_frame)

        mini_map_frame = grey_scale_frame[start_y:end_y, start_x:end_x]

        height, width = mini_map_frame.shape

        # extract the coordinates of the player position using cross needle

        player_coordinates = self.__get_mini_map_player_position(mini_map_frame)

        # cut a portion of the map based on start coordinate

        coordinate = self.__get_pixel_from_coordinate(initial_map_coordinate)

        print(str(coordinate))

        tibia_map_roi = tibia_map[coordinate.y - 200:coordinate.y + 200, coordinate.x - 200:coordinate.x + 200]

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

        # show the output image
        cv2.imshow("Output", tibia_map_roi)
        cv2.waitKey(0)

        # find on this map portion the minimap

        match = cv2.matchTemplate(tibia_map_roi, mini_map_frame, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        start_x = (coordinate.x - 200) + x + player_coordinates.x
        start_y = (coordinate.y - 200) + y + player_coordinates.y

        result = self.__get_map_coordinate_from_pixel(Coordinate(start_x, start_y), initial_map_coordinate.z)

        print(str(result))

    def __get_map_coordinate_from_pixel(self, coordinate: Coordinate, floor: int) -> MapCoordinate:
        return MapCoordinate(coordinate.x + 31744, coordinate.y + 30976, floor)
    def __get_pixel_from_coordinate(self, coordinate: MapCoordinate) -> Coordinate:
        return Coordinate(coordinate.x - 31744, coordinate.y - 30976)

    def __get_mini_map_player_position(self, mini_map_frame: np.array) -> Coordinate:
        map_position_cross = Cv2File.load_image(f'Wiki/Ui/Map/map_position_cross.png')
        match = cv2.matchTemplate(mini_map_frame, map_position_cross, cv2.TM_CCOEFF_NORMED)

        height, width = map_position_cross.shape

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        end_x = x + width
        end_y = y + height

        screen_region = ScreenRegion(x, end_x, y, end_y)

        return Coordinate.from_screen_region(screen_region)

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
