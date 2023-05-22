import numpy as np
from PathFindingPackage import Map
from .MoveCommand import MoveCommand
import time
from .Player import Player


class PathFinder:
    def execute(self, last_waypoint: str, next_waypoint: str, frame: np.array, player: Player):
        game_map = Map()

        path = game_map.find_shortest_path(last_waypoint, next_waypoint)
        print(str(path))

        while path.current is not None:
            command: MoveCommand = path.current.data

            time.sleep(1)

            player.move(command)

            path.next()

