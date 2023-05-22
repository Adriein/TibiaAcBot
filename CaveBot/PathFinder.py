import numpy as np
from PathFindingPackage import Map
from UtilPackage import LinkedList


class PathFinder:
    def __init__(self):
        self.game_map = Map()

    def execute(self, last_known_waypoint: str, destination_waypoint: str, frame: np.array) -> LinkedList:
        current_tile = self.game_map.where_am_i(last_known_waypoint, frame)
        current_waypoint = current_tile.waypoint.to_plain()

        return self.game_map.find_shortest_path(current_waypoint, destination_waypoint)
