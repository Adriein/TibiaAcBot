import json
from typing import Dict, Any
from threading import Event
from .Player import Player
from .MoveCommand import MoveCommand


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    __data = None

    def __new__(cls, script_json_data: Dict[str, Any], player: Player):
        cls.__data = script_json_data
        cls.player = player

        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)

        return cls.__INSTANCE

    @staticmethod
    def load(name: str, player: Player) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data, player)

    def start(self, walk_event: Event) -> None:
        print(self.__data['walk'])
        for command in self.__data['walk']:
            [steps, direction] = command

            move_command = MoveCommand(steps, direction)

            if not walk_event.is_set():
                walk_event.wait()

            self.player.move(move_command)



