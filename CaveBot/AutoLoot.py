import time
from LoggerPackage import Logger as TibiaAcBotLogger
from CaveBot.Player import Player
from ScreenAnalizerPackage import ScreenRegion
from ScreenAnalizerPackage import PositionError
from ScreenAnalizerPackage import Coordinate
from ScreenAnalizerPackage import Screen


class AutoLoot:
    def __init__(self, player: Player):
        self.player = player

    def loot(self) -> None:
        try:
            coordinates = self.__create_looting_area()

            for coordinate in coordinates:
                self.player.loot(coordinate)

                time.sleep(0.4)

        except PositionError:
            pass

        except Exception as exception:
            TibiaAcBotLogger.error('AUTO_LOOT_FATAL_ERROR', exception)

    def __create_looting_area(self) -> list[Coordinate]:
        screen_region = Screen.GAME_WINDOW

        if screen_region is None:
            raise Exception

        screen_region: ScreenRegion

        center_game_window_coordinate = Coordinate.from_screen_region(screen_region)

        first_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y - 44)
        second_looting_point = Coordinate(center_game_window_coordinate.x + 44, first_looting_point.y)
        third_looting_point = Coordinate(center_game_window_coordinate.x + 44, center_game_window_coordinate.y)
        fourth_looting_point = Coordinate(third_looting_point.x, third_looting_point.y + 44)
        fifth_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y + 44)
        six_looting_point = Coordinate(center_game_window_coordinate.x - 44, fifth_looting_point.y)
        seven_looting_point = Coordinate(center_game_window_coordinate.x - 44, center_game_window_coordinate.y)
        eight_looting_point = Coordinate(seven_looting_point.x, center_game_window_coordinate.y - 44)

        result = list()

        result.append(first_looting_point)
        result.append(second_looting_point)
        result.append(third_looting_point)
        result.append(fourth_looting_point)
        result.append(fifth_looting_point)
        result.append(six_looting_point)
        result.append(seven_looting_point)
        result.append(eight_looting_point)

        return result
