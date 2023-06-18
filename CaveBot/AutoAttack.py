from .BattleList import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from LoggerPackage import Logger as TibiaAcBotLogger
from .Player import Player
from .AutoLoot import AutoLoot
from threading import Event
import time
from .ScriptEnemy import ScriptEnemy

runner_enemy = False
class AutoAttack:
    def __init__(self, auto_loot: AutoLoot, player: Player, walk_event: Event, combat_event: Event,
                 creatures: list[ScriptEnemy]):
        initial_frame = WindowCapturer.start()
        self.battle_list = BattleList.create(initial_frame)
        self.auto_loot = auto_loot
        self.player = player
        self.walk_event = walk_event
        self.combat_event = combat_event
        self.creatures = creatures
        self.runner_enemy = False

    def attack(self) -> None:
        while True:
            frame = WindowCapturer.start()

            try:
                enemies_in_battle_list = self.battle_list.find_enemies(frame, self.creatures)

                self.walk_event.clear()

                self.combat_event.set()

                battle_list_attack_position = enemies_in_battle_list[0].position

                for enemy in enemies_in_battle_list:
                    self.runner_enemy = enemy.runner

                    if self.runner_enemy:
                        self.player.chase_opponent()

                    self.player.attack()

                    time.sleep(1)

                    while True:
                        actual_frame = WindowCapturer.start()

                        if not self.battle_list.is_nearest_enemy_attacked(actual_frame, battle_list_attack_position):
                            break

                    if self.runner_enemy:
                        self.auto_loot.loot()
                        self.player.not_chase_opponent()

                self.combat_event.clear()

            except NoEnemyFound:
                if self.walk_event.is_set():
                    continue

                if not self.runner_enemy:
                    self.auto_loot.loot()

                self.combat_event.clear()
                self.walk_event.set()

                continue

            except Exception as exception:
                TibiaAcBotLogger.error('AUTO_ATTACK_FATAL_ERROR', exception)
                self.combat_event.clear()
                continue
