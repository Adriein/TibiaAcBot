from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer
from .Keyboard import Keyboard
from .Player import Player
from threading import Event
import time


class AutoHealer:
    HIT_POINT_THRESHOLD = 500
    MANA_THRESHOLD = 5

    def __init__(self, player: Player):
        self.player = player

    def heal(self, combat_event: Event) -> None:
        while True:
            time.sleep(3)

            if combat_event.is_set():
                continue

            self.player.eat()

            frame = WindowCapturer.start()
            health = self.player.health(frame)

            if self.have_to_be_healed(health):
                TibiaAcBotLogger.debug(f'player healed')
                Keyboard.press('r')

    def have_to_be_healed(self, hp: int) -> bool:
        return hp <= self.HIT_POINT_THRESHOLD

    def use_mana_potion(self) -> None:
        TibiaAcBotLogger.debug(f'player used mana potion')

    def need_mana(self, mana: int) -> bool:
        return mana <= self.MANA_THRESHOLD
