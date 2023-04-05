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

            nearest_creature, *_ = creature_coords_in_battle_list

            self.battle_list.is_nearest_creature_attacked(frame, nearest_creature)

        except NoCreatureFound:
            pass

