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
            creature_coords_in_battle_list = self.battle_list.find_enemies(frame)

            actual_creatures_in_range = len(creature_coords_in_battle_list)

            self.battle_list.set_actual_creatures_in_range(actual_creatures_in_range)

            if self.__not_attacking_and_creature_in_range(player):
                nearest_creature_coords, *_ = creature_coords_in_battle_list

                player.attack(nearest_creature_coords)

                self.battle_list.set_previous_creatures_in_range(actual_creatures_in_range)

                return

            if self.__previous_creature_has_been_killed(actual_creatures_in_range):
                actual_creatures_in_range = len(creature_coords_in_battle_list)

                nearest_creature_coords, *_ = creature_coords_in_battle_list
                player.attack(nearest_creature_coords)

                BattleList.CREATURES_IN_RANGE = actual_creatures_in_range

                return

        except NoCreatureFound:
            BattleList.ACTUAL_CREATURE_IN_RANGE = 0


    def __previous_creature_has_been_killed(self, creatures: int) -> bool:
        previous_creatures = BattleList.PREVIOUS_CREATURE_IN_RANGE
        return creatures < previous_creatures

    def __not_attacking_and_creature_in_range(self, player: Player) -> bool:
        return player.IS_ATTACKING is False and self.battle_list.ACTUAL_CREATURE_IN_RANGE > 0
