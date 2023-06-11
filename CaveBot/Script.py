import json
import time
import numpy as np
from typing import Dict, Any
from .MoveCommand import MoveCommand
from UtilPackage import LinkedList


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    waypoints: LinkedList = LinkedList()
    creatures: list[str] = list()

    __previous_waypoint = None

    FLOOR_LEVEL = 5

    FLOORS_LEVELS: set[int] = set()

    def __init__(self, script_json_data):
        for creature in script_json_data['creatures']:
            self.creatures.append(creature)

        for waypoint in script_json_data['walk']:
            self.FLOORS_LEVELS.add(Script.__extract_z_level_from_waypoint(waypoint[0]))
            self.waypoints.append(waypoint)

    @staticmethod
    def load(name: str) -> 'Script':
        with open(name, Script.__READ_MODE) as file:
            data = json.load(file)

        return Script(data)

    @staticmethod
    def __extract_z_level_from_waypoint(waypoint: str) -> int:
        x, y, z = waypoint.split(',')

        return int(z)
