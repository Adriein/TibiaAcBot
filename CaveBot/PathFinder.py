import numpy as np
from .Map import Map
from UtilPackage import LinkedList


class PathFinder:
    def __init__(self):
        self.game_map = Map()

    def execute(self, last_known_waypoint: list[str], destination_waypoint: list[str], current_floor: int, frame: np.array) -> LinkedList:
        current_tile = self.game_map.where_am_i(last_known_waypoint[0], current_floor, frame)

        current_waypoint = current_tile.waypoint.to_string()

        return self.game_map.find_shortest_path(current_waypoint, destination_waypoint[0])
