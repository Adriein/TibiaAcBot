import numpy as np
from PathFindingPackage import Map


class PathFinder:
    def execute(self, last_waypoint: str, next_waypoint: str, frame: np.array):
        game_map = Map()

        path = game_map.find_shortest_path(last_waypoint, next_waypoint)

        print(str(path))

