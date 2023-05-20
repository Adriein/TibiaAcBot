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
        start_screen_coordinate = self.__get_pixel_from_waypoint(current)
        destination_screen_coordinate = self.__get_pixel_from_waypoint(destination)

        initial_direction = self.__calculate_initial_direction(current, destination)

        # determine the direction where we have to start looking
        # start a loop tracking the visited pixels and do the color logic on the pixels until reach the destination coordinate

        tibia_walkable_map = Cv2File.load_image(f'Wiki/Ui/Map/Walkable/floor-5-path.png', False)

        open_set = []
        visited = set()

        start_tile = Tile.build(current)
        start_tile.calculate_cost(destination)

        destination_tile = Tile.build(destination)

        heapq.heappush(open_set, start_tile)

        while open_set:
            current_tile: Tile = heapq.heappop(open_set)

            if current_tile == destination_tile:
                # Goal reached, construct the path
                path = []

                while current_tile:
                    path.append(current_tile)
                    current_tile = current_tile.parent

                path.reverse()

                return path

            visited.add(current_tile)

            for neighbor_tile in current_tile.adjacent_tiles:
                if neighbor_tile in visited:
                    continue

                if neighbor_tile.f_score < current_tile.f_score or neighbor_tile not in open_set:
                    neighbor_tile.parent = current_tile
                    neighbor.g_score = tentative_g_score

                    if neighbor_tile not in open_set:
                        open_set.append(neighbor_tile)

    def __string_to_waypoint(self, string_waypoint: str) -> Waypoint:
        x, y, z = string_waypoint.split(',')

        return Waypoint(x, y, z)

    def __get_map_tile_from_pixel(self, coordinate: Coordinate, floor: int) -> Tile:
        return Tile(uuid.uuid4(), Waypoint(coordinate.x + 31744, coordinate.y + 30976, floor))

    def __get_pixel_from_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)

    def __calculate_initial_direction(self, current: Waypoint, destination: Waypoint) -> str:
        if destination.x > current.x:
            if destination.y > current.y:
                return 'south-east'

            return 'north-east'

        if destination.x == current.x:
            if destination.y > current.y:
                return 'south'

            return 'north'

        if destination.y > current.y:
            return 'south-west'

        return 'north-west'

    def __create_adjacent_tiles(self, current_tile: Tile, destination: Tile) -> None:
        # 0,1 stands for x (1, -1) means move left and right
        # 2,3 stands for y (1, -1) means move up and down
        cardinality = {0: 1, 1: -1, 2: 1, 3: -1}

        for step in range(4):
            next_waypoint = Waypoint(current_tile.waypoint.x + cardinality[step])
            current_tile.add_adjacent_tile(Tile.build())
