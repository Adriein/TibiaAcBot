import json
import time
import numpy as np
from typing import Dict, Any
from threading import Event
from .Player import Player
from .MoveCommand import MoveCommand
from .PathFinder import PathFinder
from UtilPackage import LinkedList


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    __waypoints: LinkedList = LinkedList()
    creatures: list[str] = list()

    __previous_waypoint = None

    def __new__(cls, script_json_data: Dict[str, Any], player: Player, path_finder: PathFinder, walk_event: Event):
        if cls.__INSTANCE:
            return cls.__INSTANCE

        cls.__INSTANCE = super().__new__(cls)

        for creature in script_json_data['creatures']:
            cls.creatures.append(creature)

        for waypoint in script_json_data['walk']:
            cls.__waypoints.append(waypoint)

        cls.player = player
        cls.path_finder = path_finder
        cls.walk_event = walk_event

        return cls.__INSTANCE

    @staticmethod
    def load(name: str, player: Player, walk_event: Event) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data, player, PathFinder(), walk_event)

    def start(self, frame: np.array) -> None:
        if not self.walk_event.is_set():
            return

        if self.__previous_waypoint is None:
            self.__previous_waypoint = self.__waypoints.current.data

        walk_instructions = self.path_finder.execute(self.__previous_waypoint, self.__waypoints.current.data, frame)
        print(str(walk_instructions))
        while walk_instructions.current is not None:
            command: MoveCommand = walk_instructions.current.data

            time.sleep(0.8)

            self.player.move(command)

            walk_instructions.next()

        self.__previous_waypoint = self.__waypoints.current.data

        self.__waypoints.next()
