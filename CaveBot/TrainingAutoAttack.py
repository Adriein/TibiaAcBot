from .BattleList import BattleList
from ScreenAnalizerPackage import NoEnemyFound
from ScreenAnalizerPackage import WindowCapturer
from LoggerPackage import Logger as TibiaAcBotLogger
from .Player import Player
import time
from .ScriptEnemy import ScriptEnemy
from threading import Event


class TrainingAutoAttack:
    __COUNTER = 0

    def __init__(self, player: Player, creatures: list[ScriptEnemy], combat_event: Event):
        initial_frame = WindowCapturer.start()
        self.battle_list = BattleList.create(initial_frame)
        self.creatures = creatures
        self.player = player
        self.combat_event = combat_event

    def train(self) -> None:
        self.combat_event.set()

        while True:
            frame = WindowCapturer.start()

            try:
                self.player.eat()

                enemies_in_battle_list = self.battle_list.find_enemies(frame, self.creatures)

                battle_list_attack_position = enemies_in_battle_list[0].position

                for _ in enemies_in_battle_list:
                    self.player.attack()

                    time.sleep(1)

                    while True:
                        if self.__COUNTER == 50:
                            self.player.heal()
                            self.__COUNTER = 0

                        actual_frame = WindowCapturer.start()

                        self.__COUNTER = self.__COUNTER + 1

                        if not self.battle_list.is_nearest_enemy_attacked(actual_frame, battle_list_attack_position):
                            break

            except NoEnemyFound:
                continue

            except Exception as exception:
                TibiaAcBotLogger.error('AUTO_ATTACK_FATAL_ERROR', exception)

                raise exception
