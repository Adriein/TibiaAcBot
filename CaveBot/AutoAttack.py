from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from .Player import Player
from .Enemy import Enemy
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

    def attack(self, frame_queue: Queue, walk_event: Event, combat_event: Event) -> None:
        frame = frame_queue.get()

        try:
            creature_coords_in_battle_list = self.battle_list.find_enemies(frame)

            combat_event.set()

            nearest_creature = Enemy('mountain_troll', creature_coords_in_battle_list[0])

            creature_click_coordinate = nearest_creature.click_coords()

            cv2.drawMarker(frame, (creature_click_coordinate.x, creature_click_coordinate.y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)

            if not self.battle_list.is_nearest_enemy_attacked(frame, nearest_creature.position):
                self.player.attack(creature_click_coordinate)

                time.sleep(1)

        except NoEnemyFound:
            combat_event.clear()
            return

        except Exception as exception:
            print(exception)
            return

