import numpy as np
import uuid
import cv2
import math
from UtilPackage import LinkedList
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File
from ScreenAnalizerPackage import Coordinate
from CaveBot.MoveCommand import MoveCommand
from CaveBot.Script import Script
from .Tile import Tile
from .Waypoint import Waypoint
from .AStar import AStar


class Map:
    def __init__(self):
        self.path_finding_algorithm = AStar()

    def where_am_i(self, last_waypoint: str, frame: np.array) -> Tile:
        last_waypoint = self.__string_to_waypoint(last_waypoint)

        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-{Script.FLOOR_LEVEL}.png')

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

        return self.__get_map_tile_from_pixel(Coordinate(start_x, start_y), last_waypoint.z)

    def find_shortest_path(self, current_waypoint: str, destination_waypoint: str) -> LinkedList:
        current_waypoint = self.__string_to_waypoint(current_waypoint)
        destination_waypoint = self.__string_to_waypoint(destination_waypoint)

        tile_path = self.path_finding_algorithm.execute(current_waypoint, destination_waypoint)
        print('destination waypoint?')
        print(destination_waypoint)
        print('path:')
        print(str(tile_path))

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
