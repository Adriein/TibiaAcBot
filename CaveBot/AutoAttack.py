from .BattleList import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from ScreenAnalizerPackage import Scanner
from LoggerPackage import Logger as TibiaAcBotLogger
from .Player import Player
from .AutoLoot import AutoLoot
from .Enemy import Enemy
from threading import Event
import time
import numpy as np
import cv2
from .ScriptEnemy import ScriptEnemy

runner_enemy = False


class AutoAttack:
    def __init__(self, auto_loot: AutoLoot, player: Player, walk_event: Event, combat_event: Event, creatures: list[ScriptEnemy], force_ring: bool):
        initial_frame = WindowCapturer.start()
        self.battle_list = BattleList.create(initial_frame)
        self.auto_loot = auto_loot
        self.player = player
        self.walk_event = walk_event
        self.combat_event = combat_event
        self.creatures = creatures
        self.runner_enemy = False
        self.force_ring = force_ring

    def attack(self) -> None:
        while True:
            frame = WindowCapturer.start()

            try:
                enemies_in_battle_list = self.battle_list.find_enemies(frame, self.creatures)

                self.walk_event.clear()

                self.combat_event.set()

                battle_list_attack_position = enemies_in_battle_list[0].position

                for enemy in enemies_in_battle_list:
                    if self.force_ring and not self.__is_stealth_ring_on(frame):
                        print('use ring')
                        self.player.use_stealth_ring()

                    self.runner_enemy = enemy.runner

                    self.__activate_chase_opponent(enemy)

                    self.player.attack()

                    self.player.heal()

                    time.sleep(1)

                    while True:
                        actual_frame = WindowCapturer.start()

                        if not self.battle_list.is_nearest_enemy_attacked(actual_frame, battle_list_attack_position):
                            break

                    if self.runner_enemy:
                        if enemy.loot:
                            self.auto_loot.loot()

                        self.player.not_chase_opponent()

                self.combat_event.clear()

            except NoEnemyFound:
                if self.walk_event.is_set():
                    continue

                if not self.runner_enemy:
                    self.auto_loot.loot()

                self.player.eat()
                self.combat_event.clear()
                self.walk_event.set()

                continue

            except Exception as exception:
                TibiaAcBotLogger.error('AUTO_ATTACK_FATAL_ERROR', exception)
                self.combat_event.clear()
                continue

    def __is_chasing_opponent_activated(self, frame: np.array) -> bool:
        (start_x, end_x, start_y, end_y) = Scanner.combat_stance_position(frame)

        frame_roi = frame[start_y:end_y, start_x:end_x]

        hsv_image = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for green color in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        # Create a mask based on the color threshold
        mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # Count the number of green pixels
        green_pixel_count = cv2.countNonZero(mask)

        # Determine if the image contains green color
        if green_pixel_count > 0:
            return True

        return False

    def __activate_chase_opponent(self, enemy: Enemy) -> None:
        frame = WindowCapturer.start()

        if not self.__is_chasing_opponent_activated(frame) and enemy.runner:
            self.player.chase_opponent()

    def __is_stealth_ring_on(self, frame: np.array) -> bool:
        (start_x, end_x, start_y, end_y) = Scanner.ring_position(frame)

        frame_roi = frame[start_y:end_y, start_x:end_x]

        hsv_image = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Define the RGB value of the color red that are counter of the ring
        color_to_find = (191, 0, 0)

        # Check if the color is similar to the target color
        color_found = np.all(hsv_image == color_to_find, axis=-1).any()

        print(color_found)

        # Determine if the image contains blue color
        return color_found
