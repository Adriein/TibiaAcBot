from FilesystemPackage import Cv2File
from ScreenAnalizerPackage import Coordinate
from .Tile import Tile
from .Waypoint import Waypoint
import numpy as np
import heapq
import cv2


class AStar:
    def __init__(self):
        '''
        I need to iterate to all the waypoints of the script in order to cache all the floors that i should visit during
        the duration of the script
        '''
        tibia_walkable_map_floor_5 = Cv2File.load_image(f'Wiki/Ui/Map/Walkable/floor-5-path.png', False)
        tibia_walkable_map_floor_6 = Cv2File.load_image(f'Wiki/Ui/Map/Walkable/floor-6-path.png', False)

        self.tibia_walkable_map_hsv_floor_5 = cv2.cvtColor(tibia_walkable_map_floor_5, cv2.COLOR_BGR2HSV)
        self.tibia_walkable_map_hsv_floor_6 = cv2.cvtColor(tibia_walkable_map_floor_6, cv2.COLOR_BGR2HSV)

    def execute(self, current: Waypoint, destination: Waypoint) -> list[Tile]:
        open_set = []
        visited = set()

        start_tile = Tile.build(current)
        start_tile.calculate_cost(current, destination)

        destination_tile = Tile.build(destination)

        heapq.heappush(open_set, start_tile)

        while open_set:
            current_tile: Tile = heapq.heappop(open_set)

            if current_tile == destination_tile:
                path = list()

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

                if self.__is_not_walkable_waypoint(neighbor_tile):
                    visited.add(neighbor_tile)
                    continue

                neighbor_tile.calculate_cost(current, destination)

                if neighbor_tile.f_score < current_tile.f_score or neighbor_tile not in open_set:
                    neighbor_tile.parent = current_tile

                    if neighbor_tile not in open_set:
                        open_set.append(neighbor_tile)

    def __is_not_walkable_waypoint(self, current: Tile) -> bool:
        # Define the lower and upper bounds of the yellow color range in BGR format
        lower_yellow = np.array([0, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([100, 255, 255], dtype=np.uint8)

        pixel = self.__get_pixel_from_waypoint(current.waypoint)

        pixel_color = None

        if current.waypoint.z == 5:
            pixel_color = self.tibia_walkable_map_hsv_floor_5[pixel.y, pixel.x]

        if current.waypoint.z == 6:
            pixel_color = self.tibia_walkable_map_hsv_floor_6[pixel.y, pixel.x]

        mask = cv2.inRange(pixel_color, lower_yellow, upper_yellow)

        return np.all(mask == 255)

    def __get_pixel_from_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)