from ScreenAnalizerPackage import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from LoggerPackage import Logger as TibiaAcBotLogger
from .Player import Player
from .Enemy import Enemy
from .AutoLoot import AutoLoot
from threading import Event
import time


class AutoAttack:
    def __init__(self, auto_loot: AutoLoot, player: Player, walk_event: Event, combat_event: Event, creatures: list[str]):
        initial_frame = WindowCapturer.start()
        self.battle_list = BattleList.create(initial_frame)
        self.auto_loot = auto_loot
        self.player = player
        self.walk_event = walk_event
        self.combat_event = combat_event
        self.creatures = creatures

    def attack(self) -> None:
        while True:
            frame = WindowCapturer.start()

            try:
                creature_coords_in_battle_list = self.battle_list.find_enemies(frame, self.creatures)

                self.walk_event.clear()

                self.combat_event.set()

                nearest_creature = Enemy('mountain_troll', creature_coords_in_battle_list[0])

                battle_list_attack_position = nearest_creature.position

                for _ in creature_coords_in_battle_list:
                    self.player.attack()

                    time.sleep(0.6)

                    while True:
                        actual_frame = WindowCapturer.start()

                        if not self.battle_list.is_nearest_enemy_attacked(actual_frame, battle_list_attack_position):
                            break

            except NoEnemyFound:
                if self.walk_event.is_set():
                    continue

                self.auto_loot.loot()

                self.combat_event.clear()
                self.walk_event.set()

                continue

            except Exception as exception:
                TibiaAcBotLogger.error('AUTO_ATTACK_FATAL_ERROR', exception)
                self.combat_event.clear()
                continue
