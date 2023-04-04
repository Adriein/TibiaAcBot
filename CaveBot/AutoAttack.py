from ScreenAnalizerPackage import BattleList
import numpy as np


class AutoAttack:
    @staticmethod
    def start(frame: np.array) -> None:
        battle_list = BattleList.create()

        (x, y) = battle_list.get_coordinates_of_nearest_creature(frame)
