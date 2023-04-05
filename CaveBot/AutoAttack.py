from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoCreatureFound
from LoggerPackage import Logger
from .Player import Player
import numpy as np


class AutoAttack:
    @staticmethod
    def start(frame: np.array) -> 'AutoAttack':
        battle_list = BattleList.create(frame)

        return AutoAttack(battle_list)

    def __init__(self, battle_list: BattleList):
        self.battle_list = battle_list

    def attack(self, frame, player: Player) -> None:
        try:
            creature_coords_in_battle_list = self.battle_list.inspect(frame)

            if self.__not_attacking_and_creature_in_range(creature_coords_in_battle_list):
                print('first if')
                actual_creatures_in_range = len(creature_coords_in_battle_list)
                print('actual_creatures_in_range')
                print(actual_creatures_in_range)
                nearest_creature_coords, *_ = creature_coords_in_battle_list
                player.attack(nearest_creature_coords)

                BattleList.CREATURES_IN_RANGE = actual_creatures_in_range

                return

            if self.__previous_creature_has_been_killed(creature_coords_in_battle_list):
                print('second if')
                actual_creatures_in_range = len(creature_coords_in_battle_list)
                print('actual_creatures_in_range')
                print(actual_creatures_in_range)
                nearest_creature_coords, *_ = creature_coords_in_battle_list
                player.attack(nearest_creature_coords)

                BattleList.CREATURES_IN_RANGE = actual_creatures_in_range

                return

        except NoCreatureFound:
            Logger.debug('No creature found in battle list')
            self.battle_list.change_creature_in_range_counter(0)


    def __previous_creature_has_been_killed(self, creature_coords_in_battle_list: list[tuple[int, int]]) -> bool:
        return len(creature_coords_in_battle_list) < BattleList.CREATURES_IN_RANGE

    def __not_attacking_and_creature_in_range(self, creature_coords_in_battle_list: list[tuple[int, int]]) -> bool:
        return BattleList.CREATURES_IN_RANGE == 0 and len(creature_coords_in_battle_list) > 0
