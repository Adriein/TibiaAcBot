import json
from typing import Dict, Any
from threading import Event
from .Player import Player
from .MoveCommand import MoveCommand
from UtilPackage import LinkedList


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    __data: LinkedList = LinkedList()

    def __new__(cls, script_json_data: Dict[str, Any], player: Player):
        if cls.__INSTANCE:
            return cls.__INSTANCE

        cls.__INSTANCE = super().__new__(cls)

        for command in script_json_data['walk']:
            [steps, direction] = command

            cls.__data.append(MoveCommand(steps, direction))

        cls.player = player

        return cls.__INSTANCE

    @staticmethod
    def load(name: str, player: Player) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data, player)

    def start(self, walk_event: Event) -> None:
        if not walk_event.is_set():
            return

        while self.__data.current is not None:
            command: MoveCommand = self.__data.current.data

            self.player.move(command)

            self.__data.next()



