from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from ScreenAnalizerPackage import ScreenRegion
from .Player import Player
from .Enemy import Enemy
import queue
from queue import Queue
from threading import Event
import time
import cv2


class AutoAttack:
    @staticmethod
    def start(player: Player) -> 'AutoAttack':
        initial_frame = WindowCapturer.start()

        battle_list = BattleList.create(initial_frame)

        return AutoAttack(battle_list, player)

    def __init__(self, battle_list: BattleList, player: Player):
        self.battle_list = battle_list
        self.player = player

    def attack(self, frame_queue: Queue, stop_walk_event: Event, processed_frame_queue: Queue) -> None:
        while True:
            try:
                frame = frame_queue.get()

                creature_coords_in_battle_list = self.battle_list.find_enemies(frame)

                if self.__are_enemies_in_range(creature_coords_in_battle_list):
                    stop_walk_event.set()

                nearest_creature = Enemy('mountain_troll', creature_coords_in_battle_list[0])

                creature_click_coordinate = nearest_creature.click_coords()

                cv2.drawMarker(frame, (creature_click_coordinate.x, creature_click_coordinate.y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)

                if not self.battle_list.is_nearest_enemy_attacked(frame, nearest_creature.position):
                    self.player.attack(creature_click_coordinate)

                    time.sleep(1)

                processed_frame_queue.put(frame)

            except NoEnemyFound:
                pass

    def __are_enemies_in_range(self, creatures: list[ScreenRegion]) -> bool:
        return len(creatures) > 0

