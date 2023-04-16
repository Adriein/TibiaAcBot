from ScreenAnalizerPackage import HitPoint
from ScreenAnalizerPackage import Mana
from ScreenAnalizerPackage import Position
from ScreenAnalizerPackage import Coordinate
from LoggerPackage import Logger
from .Keyboard import Keyboard
from .Mouse import Mouse
from .AutoHealer import AutoHealer
import time
import numpy as np


class Player:
    @staticmethod
    def create() -> 'Player':
        return Player(HitPoint(), Mana(), AutoHealer(), Mouse())

    def __init__(self, hp: HitPoint, mana_bar: Mana, auto_healer: AutoHealer, mouse: Mouse):
        self.hp = hp
        self.mana_bar = mana_bar
        self.auto_healer = auto_healer
        self.mouse = mouse

    # STATS
    def health(self) -> int:
        player_health = self.hp.get()
        Logger.debug(f'health: {player_health}')

        return player_health

    def watch_health(self) -> None:
        while True:
            time.sleep(3)
            current_hp = self.health()

            if self.auto_healer.have_to_be_healed(current_hp):
                self.auto_healer.heal()

    def mana(self) -> int:
        player_mana = self.mana_bar.get()
        Logger.debug(f'mana: {player_mana}')
        return player_mana

    def watch_mana(self) -> None:
        while True:
            time.sleep(3)
            current_mana = self.mana()

            if self.auto_healer.need_mana(current_mana):
                self.auto_healer.use_mana_potion()

    # ACTIONS
    def attack(self, coordinates: Coordinate) -> None:
        self.mouse.use_left_button(coordinates)

    def loot(self, coordinates: Coordinate) -> None:
        self.mouse.use_right_button(coordinates)

    # MOVEMENT

    def position(self, frame: np.array) -> Position:
        return Position.check(frame)

    def move_north(self) -> None:
        Logger.debug('try to move north')
        Keyboard.press('w')
