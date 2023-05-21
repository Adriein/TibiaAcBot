from UtilPackage import LinkedList
from FilesystemPackage import Cv2File
from ScreenAnalizerPackage import Coordinate
from .Tile import Tile
from .Waypoint import Waypoint
import numpy as np
import heapq
import cv2


class AStar:
    def execute(self, current: Waypoint, destination: Waypoint) -> LinkedList:
        open_set = []
        visited = set()

        start_tile = Tile.build(current)
        start_tile.calculate_cost(current, destination)

        destination_tile = Tile.build(destination)

        heapq.heappush(open_set, start_tile)

        while open_set:
            current_tile: Tile = heapq.heappop(open_set)

            if current_tile == destination_tile:
                path = LinkedList()

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

                print(self.__is_walkable_waypoint(neighbor_tile))
                if not self.__is_walkable_waypoint(neighbor_tile):
                    visited.add(neighbor_tile)
                    continue

                neighbor_tile.calculate_cost(current, destination)

                if neighbor_tile.f_score < current_tile.f_score or neighbor_tile not in open_set:
                    neighbor_tile.parent = current_tile

                    if neighbor_tile not in open_set:
                        open_set.append(neighbor_tile)

    def __is_walkable_waypoint(self, current: Tile) -> bool:
        tibia_walkable_map = Cv2File.load_image(f'Wiki/Ui/Map/Walkable/floor-5-path.png', False)

        tibia_walkable_map_hsv = cv2.cvtColor(tibia_walkable_map, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds of the yellow color range in BGR format
        lower_yellow = np.array([0, 150, 150], dtype=np.uint8)
        upper_yellow = np.array([100, 255, 255], dtype=np.uint8)

        pixel = self.__get_pixel_from_waypoint(current.waypoint)

        pixel_color = tibia_walkable_map_hsv[pixel.y, pixel.x]

        mask = cv2.inRange(pixel_color, lower_yellow, upper_yellow)
        print(str(current))
        return np.any(mask == 255)

    def __get_pixel_from_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)
