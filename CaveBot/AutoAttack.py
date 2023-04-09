from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from .Player import Player
from .Enemy import Enemy
import numpy as np
import time
import cv2


class AutoAttack:
    @staticmethod
    def start(frame: np.array, player: Player) -> 'AutoAttack':
        battle_list = BattleList.create(frame)

        return AutoAttack(battle_list, player)

    def __init__(self, battle_list: BattleList, player: Player):
        self.battle_list = battle_list
        self.player = player

    def attack(self, frame: np.array) -> None:
        try:
            creature_coords_in_battle_list = self.battle_list.find_enemies(frame)

            nearest_creature = Enemy('mountain_troll', creature_coords_in_battle_list[0])

            if not self.battle_list.is_nearest_enemy_attacked(frame, nearest_creature.position):
                creature_click_coordinate = nearest_creature.click_coords()

                self.player.attack(creature_click_coordinate)

                cv2.drawMarker(frame, (creature_click_coordinate.x, creature_click_coordinate.y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)

                time.sleep(2)

        except NoEnemyFound:
            pass
