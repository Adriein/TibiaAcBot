import json
from UtilPackage import LinkedList
from .ScriptEnemy import ScriptEnemy


class Script:
    __INSTANCE = None
    __READ_MODE = 'r'

    waypoints: LinkedList = LinkedList()
    creatures: list[ScriptEnemy] = list()

    __previous_waypoint = None

    FLOOR_LEVEL = 8

    FLOORS_LEVELS: set[int] = set()

    def __init__(self, script_json_data):
        for creature in script_json_data['creatures']:
            print(creature)
            self.creatures.append(ScriptEnemy(creature.name, creature.runner))

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
