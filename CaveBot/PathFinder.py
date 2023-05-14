import numpy as np
from PathFindingPackage import Map


class PathFinder:
    def execute(self, last_waypoint: str, nest_waypoint: str, frame: np.array):
        game_map = Map()

        tile = game_map.where_am_i(last_waypoint, frame)

