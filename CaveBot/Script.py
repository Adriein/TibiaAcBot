import json
import time
import numpy as np
from typing import Dict, Any
from .MoveCommand import MoveCommand
from UtilPackage import LinkedList


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    __waypoints: LinkedList = LinkedList()
    creatures: list[str] = list()

    __previous_waypoint = None

    FLOOR_LEVEL = 5

    FLOORS_LEVELS: set[int] = set()

    def __new__(cls, script_json_data: Dict[str, Any]):
        if cls.__INSTANCE:
            return cls.__INSTANCE

        cls.__INSTANCE = super().__new__(cls)

        for creature in script_json_data['creatures']:
            cls.creatures.append(creature)

        for waypoint in script_json_data['walk']:
            cls.FLOORS_LEVELS.add(Script.__extract_z_level_from_waypoint(waypoint))
            cls.__waypoints.append(waypoint)

        return cls.__INSTANCE

    @staticmethod
    def load(name: str) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data)

    @staticmethod
    def __extract_z_level_from_waypoint(waypoint: str) -> int:
        x, y, z = waypoint.split(',')

        return int(z)

    def start(self, frame: np.array) -> None:
        if not self.walk_event.is_set():
            return

        if self.__previous_waypoint is None:
            self.__previous_waypoint = self.__waypoints.current.data

        walk_instructions = self.path_finder.execute(self.__previous_waypoint, self.__waypoints.current.data,
                                                     Script.FLOOR_LEVEL, frame)

        while walk_instructions.current is not None:
            command: MoveCommand = walk_instructions.current.data

            time.sleep(0.8)

            self.player.move(command)

            walk_instructions.next()

        try:
            waypoint_type = self.__waypoints.current.data[1]

            if waypoint_type == 'stairDown':
                Script.FLOOR_LEVEL = Script.FLOOR_LEVEL + 1

            if waypoint_type == 'stairUp':
                Script.FLOOR_LEVEL = Script.FLOOR_LEVEL - 1

        except IndexError:
            pass

        self.__previous_waypoint = self.__waypoints.current.data

        self.__waypoints.next()

        if self.__waypoints.has_to_reset():
            self.__waypoints.reset()

        time.sleep(0.5)
