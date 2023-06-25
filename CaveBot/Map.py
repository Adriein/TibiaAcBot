import numpy as np
import uuid
import cv2
import math
from UtilPackage import LinkedList
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File
from ScreenAnalizerPackage import Coordinate
from .MoveCommand import MoveCommand
from .Tile import Tile
from .Waypoint import Waypoint
from .AStar import AStar


class Map:
    FALSE_NON_WALKABLE_POSITIVES = [
        "32439, 32308, 8",
        "32435, 32295, 8",
        "32423, 32303, 8",
        "32429, 32306, 8",
        "32430, 32302, 8",
        "32444, 32295, 9",
        "32444, 32294, 9",
        "32444, 32293, 9",
        "32883, 32066, 9",
        "32828, 32107, 9",
        "32828, 32107, 9",
        "32917 ,32187, 8",
        "32933, 32173, 9",
        "32894, 31905, 8",
        "32822,31933,6",
        "32828,31927,6",
        "32845,31922,6",


    ]

    def __init__(self):
        self.IGNORE_WAYPOINTS = list()

        for waypoint in self.FALSE_NON_WALKABLE_POSITIVES:
            self.IGNORE_WAYPOINTS.append(self.__string_to_waypoint(waypoint))

        self.path_finding_algorithm = AStar(self.IGNORE_WAYPOINTS)

    def where_am_i(self, last_waypoint: str, current_floor: int, frame: np.array) -> Tile:
        last_waypoint = self.__string_to_waypoint(last_waypoint)

        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-{current_floor}.png')

        # find position of minimap in the screen

        (start_x, end_x, start_y, end_y) = Scanner.mini_map_position(grey_scale_frame)

        mini_map_frame = grey_scale_frame[start_y:end_y, start_x:end_x]

        height, width = mini_map_frame.shape

        # cut a portion of the map based on last waypoint

        pixel_on_map = self.__get_pixel_from_waypoint(last_waypoint)

        map_start_x = pixel_on_map.x - (math.floor(width / 2) + 20)
        map_end_x = pixel_on_map.x + (math.floor(width / 2) + 20)

        map_start_y = pixel_on_map.y - (math.floor(height / 2) + 20)
        map_end_y = pixel_on_map.y + (math.floor(height / 2) + 1 + 20)

        tibia_map_roi = tibia_map[map_start_y:map_end_y, map_start_x:map_end_x]

        # find on this map portion the minimap

        match = cv2.matchTemplate(tibia_map_roi, mini_map_frame, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        start_x = pixel_on_map.x - 20 + x
        start_y = pixel_on_map.y - 20 + y

        return self.__get_map_tile_from_pixel(Coordinate(start_x, start_y), current_floor)

    def find_shortest_path(self, current_waypoint: str, destination_waypoint: str) -> LinkedList:
        current_waypoint = self.__string_to_waypoint(current_waypoint)
        destination_waypoint = self.__string_to_waypoint(destination_waypoint)

        tile_path = self.path_finding_algorithm.execute(current_waypoint, destination_waypoint)

        if tile_path is None:
            return []

        path = LinkedList()

        for index, current_tile in enumerate(tile_path):
            try:
                destination_tile = tile_path[index + 1]

                direction = self.__waypoints_to_cardinal_direction(current_tile, destination_tile)
                path.append(MoveCommand(1, direction))
            except IndexError:
                pass

        return path

    def __string_to_waypoint(self, string_waypoint: str) -> Waypoint:
        x, y, z = string_waypoint.split(',')

        return Waypoint(int(x), int(y), int(z))

    def __get_map_tile_from_pixel(self, coordinate: Coordinate, floor: int) -> Tile:
        return Tile(uuid.uuid4(), Waypoint(coordinate.x + 31744, coordinate.y + 30976, floor))

    def __get_pixel_from_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)

    def __waypoints_to_cardinal_direction(self, current: Tile, destination: Tile) -> str:
        if destination.waypoint.x > current.waypoint.x:
            return 'east'

        if destination.waypoint.x < current.waypoint.x:
            return 'west'

        if destination.waypoint.y < current.waypoint.y:
            return 'north'

        if destination.waypoint.y > current.waypoint.y:
            return 'south'
