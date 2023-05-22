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

    def __new__(cls, script_json_data: Dict[str, Any], player: Player, path_finder: PathFinder):
        if cls.__INSTANCE:
            return cls.__INSTANCE

        cls.__INSTANCE = super().__new__(cls)

        for creature in script_json_data['creatures']:
            cls.creatures.append(creature)

        for command in script_json_data['walk']:
            [steps, direction] = command

            move_command = MoveCommand(steps, direction)

            for step in range(move_command.steps):
                cls.__waypoints.append(MoveCommand(steps, direction))

        cls.player = player
        cls.path_finder = path_finder

        return cls.__INSTANCE

    @staticmethod
    def load(name: str, player: Player) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data, player, PathFinder())

    def start(self, walk_event: Event, frame: np.array) -> None:
        while self.__waypoints.current is not None:
            if not walk_event.is_set():
                continue

            walk_instructions = self.path_finder.execute(self.__previous_waypoint, self.__waypoints.current.data, frame)

            while walk_instructions.current is not None:
                command: MoveCommand = walk_instructions.current.data

                time.sleep(0.8)

                self.player.move(command)

            self.__previous_waypoint = self.__waypoints.current.data

            self.__waypoints.next()
