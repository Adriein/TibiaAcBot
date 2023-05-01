import json
import time
from typing import Dict, Any
from threading import Event
from .Player import Player
from .MoveCommand import MoveCommand
from UtilPackage import LinkedList


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    __waypoints: LinkedList = LinkedList()
    creatures: list[str] = list()

    def __new__(cls, script_json_data: Dict[str, Any], player: Player):
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

        return cls.__INSTANCE

    @staticmethod
    def load(name: str, player: Player) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data, player)

    def start(self, walk_event: Event) -> None:
        while self.__waypoints.current is not None:
            if not walk_event.is_set():
                continue

            command: MoveCommand = self.__waypoints.current.data

            time.sleep(0.6)

            self.player.move(command)

            self.__waypoints.next()
