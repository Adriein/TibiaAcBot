from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoCreatureFound
from ScreenAnalizerPackage import Coordinate
from LoggerPackage import Logger
from .Player import Player
import numpy as np
import time

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

            nearest_creature, *_ = creature_coords_in_battle_list

            if not self.battle_list.is_nearest_creature_attacked(frame, nearest_creature):
                creature_click_coordinate = Coordinate.from_screen_region(nearest_creature)

                player.attack(creature_click_coordinate)

                time.sleep(2)

        except NoCreatureFound:
            pass
