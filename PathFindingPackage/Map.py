from typing import Any

import numpy as np
import uuid
import cv2
import math
import heapq
from ScreenAnalizerPackage import Scanner
from FilesystemPackage import Cv2File
from ScreenAnalizerPackage import Coordinate
from .Tile import Tile
from .Waypoint import Waypoint
from .MapGraph import MapGraph


class Map:
    def where_am_i(self, last_waypoint: str, frame: np.array) -> Tile:
        last_waypoint = Waypoint(32063, 31884, 5)
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tibia_map = Cv2File.load_image(f'Wiki/Ui/Map/Floors/floor-5.png')

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

    def find_shortest_path(self, current_waypoint: str, destination_waypoint: str) -> list[Tile]:
        current_waypoint = self.__string_to_waypoint(current_waypoint)
        destination_waypoint = self.__string_to_waypoint(destination_waypoint)

        self.__create_graph_between_waypoints(current_waypoint, destination_waypoint)

        return []

    def __create_graph_between_waypoints(self, current: Waypoint, destination: Waypoint) -> Any:
        open_set = []
        visited = set()

        start_tile = Tile.build(current)
        start_tile.calculate_cost(current, destination)

        destination_tile = Tile.build(destination)

        heapq.heappush(open_set, start_tile)

        while open_set:
            current_tile: Tile = heapq.heappop(open_set)

            if current_tile == destination_tile:
                path = []

                while current_tile:
                    path.append(current_tile)
                    current_tile = current_tile.parent

                path.reverse()

                return path

            visited.add(current_tile)

            current_tile.create_adjacent_tiles()

            for neighbor_tile in current_tile.adjacent_tiles:
                if neighbor_tile in visited:
                    continue

                if not self.__is_walkable_waypoint(neighbor_tile):
                    visited.add(neighbor_tile)

                neighbor_tile.calculate_cost(current, destination)

                if neighbor_tile.f_score < current_tile.f_score or neighbor_tile not in open_set:
                    neighbor_tile.parent = current_tile

                    if neighbor_tile not in open_set:
                        open_set.append(neighbor_tile)

    def __string_to_waypoint(self, string_waypoint: str) -> Waypoint:
        x, y, z = string_waypoint.split(',')

        return Waypoint(x, y, z)

    def __get_map_tile_from_pixel(self, coordinate: Coordinate, floor: int) -> Tile:
        return Tile(uuid.uuid4(), Waypoint(coordinate.x + 31744, coordinate.y + 30976, floor))

    def __get_pixel_from_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)

    def __is_walkable_waypoint(self, current: Tile) -> bool:
        tibia_walkable_map = Cv2File.load_image(f'Wiki/Ui/Map/Walkable/floor-5-path.png', False)

        # Define the lower and upper bounds of the yellow color range in BGR format
        lower_yellow = np.array([0, 150, 150])
        upper_yellow = np.array([100, 255, 255])

        pixel = self.__get_pixel_from_waypoint(current.waypoint)

        pixel_color = tibia_walkable_map[pixel.y, pixel.x]

        if cv2.inRange(pixel_color, lower_yellow, upper_yellow):
            return False

        return True
