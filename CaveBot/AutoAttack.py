from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from .Player import Player
from .Enemy import Enemy
from queue import Queue
from threading import Event
import time
import cv2
import numpy as np


class AutoAttack:
    def __init__(self, player: Player, walk_event: Event, combat_event: Event, creatures: list[str]):
        initial_frame = WindowCapturer.start()
        self.battle_list = BattleList.create(initial_frame)
        self.player = player
        self.walk_event = walk_event
        self.combat_event = combat_event
        self.creatures = creatures

    def attack(self, frame: np.array) -> None:
        try:
            creature_coords_in_battle_list = self.battle_list.find_enemies(frame, self.creatures)

            self.walk_event.clear()

            self.combat_event.set()

            nearest_creature = Enemy('mountain_troll', creature_coords_in_battle_list[0])

            creature_click_coordinate = nearest_creature.click_coords()

            cv2.drawMarker(frame, (creature_click_coordinate.x, creature_click_coordinate.y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)

            if not self.battle_list.is_nearest_enemy_attacked(frame, nearest_creature.position):
                self.player.attack(creature_click_coordinate)

                time.sleep(1)

        except NoEnemyFound:
            self.combat_event.clear()
            return

