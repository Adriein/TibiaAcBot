from ScreenAnalizerPackage import HitPoint
from ScreenAnalizerPackage import Mana
from ScreenAnalizerPackage import Position
from ScreenAnalizerPackage import Coordinate
from LoggerPackage import Logger
from .Keyboard import Keyboard
from .Mouse import Mouse
from .MoveCommand import MoveCommand
import numpy as np

class Player:
    @staticmethod
    def create() -> 'Player':
        return Player(HitPoint(), Mana(), Mouse())

    def __init__(self, hp: HitPoint, mana_bar: Mana, mouse: Mouse):
        self.hp = hp
        self.mana_bar = mana_bar
        self.mouse = mouse

    # STATS
    def health(self, frame: np.array) -> int:
        player_health = self.hp.get(frame)

        return player_health

    def mana(self, frame: np.array) -> int:
        player_mana = self.mana_bar.get(frame)
        Logger.debug(f'mana: {player_mana}')
        return player_mana

    # ACTIONS
    def attack(self, coordinates: Coordinate) -> None:
        self.mouse.use_left_button(coordinates)

    def rope(self, coordinates: Coordinate) -> None:
        Keyboard.press('f')
        self.mouse.use_left_button(coordinates)

    def eat(self) -> None:
        Keyboard.press('v')

    def loot(self, coordinates: Coordinate) -> None:
        self.mouse.use_right_button(coordinates)

    # MOVEMENT

    def position(self, frame: np.array) -> Position:
        return Position.check(frame)

    def move(self, command: MoveCommand) -> None:
        Keyboard.press(command.key)
