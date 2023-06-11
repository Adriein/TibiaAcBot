from UtilPackage import LinkedList
from ScreenAnalizerPackage import WindowCapturer
from .Script import Script
from .Player import Player
from .PathFinder import PathFinder
from .MoveCommand import MoveCommand

import time
from threading import Event


class AutoWalk:
    __INSTANCE = None

    __waypoints: LinkedList = LinkedList()
    __previous_waypoint = None

    FLOOR_LEVEL = 5

    FLOORS_LEVELS: set[int] = set()

    def __new__(cls, script: Script, player: Player):
        if cls.__INSTANCE:
            return cls.__INSTANCE

        cls.__INSTANCE = super().__new__(cls)

        cls.__waypoints = script.waypoints
        cls.player = player
        cls.path_finder = PathFinder()

        return cls.__INSTANCE

    def start(self, walking_event: Event) -> None:
        while True:
            walking_event.wait()

            frame = WindowCapturer.start()

            if self.__previous_waypoint is None:
                self.__previous_waypoint = self.__waypoints.current.data

            walk_instructions = self.path_finder.execute(
                self.__previous_waypoint,
                self.__waypoints.current.data,
                self.FLOOR_LEVEL,
                frame
            )

            while walk_instructions.current is not None:
                walking_event.wait()

                command: MoveCommand = walk_instructions.current.data

                time.sleep(0.8)

                self.player.move(command)

                walk_instructions.next()

            try:
                waypoint_type = self.__waypoints.current.data[1]

                if waypoint_type == 'stairDown':
                    self.FLOOR_LEVEL = self.FLOOR_LEVEL + 1

                if waypoint_type == 'stairUp':
                    self.FLOOR_LEVEL = self.FLOOR_LEVEL - 1

            except IndexError:
                pass

            self.__previous_waypoint = self.__waypoints.current.data

            self.__waypoints.next()

            if self.__waypoints.has_to_reset():
                self.__waypoints.reset()

            time.sleep(0.5)
