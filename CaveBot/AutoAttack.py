from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoCreatureFound
from .Player import Player
import numpy as np


class AutoAttack:
    @staticmethod
    def start(frame: np.array) -> 'AutoAttack':
        try:
            battle_list = BattleList.create(frame)

            return AutoAttack(battle_list)
        except NoCreatureFound:
            pass

    def __init__(self, battle_list: BattleList):
        self.battle_list = battle_list

    def attack(self, frame, player: Player) -> None:
        coords = self.battle_list.get_coordinates_of_nearest_creature(frame)

        player.attack(coords)



