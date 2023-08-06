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
        return Player(Mouse())

    def __init__(self, mouse: Mouse):
        self.mouse = mouse

    # ACTIONS
    def heal(self) -> None:
        Keyboard.press('r')

    def attack(self) -> None:
        Keyboard.press('space')
        # self.mouse.use_left_button(coordinates)

    def precision_attack(self, coordinates: Coordinate) -> None:
        self.mouse.use_left_button(coordinates)

    def rope(self, coordinates: Coordinate) -> None:
        Keyboard.press('f')
        self.mouse.use_left_button(coordinates)

    def use_hand_stair(self, coordinates: Coordinate) -> None:
        self.mouse.use_right_button(coordinates)

    def eat(self) -> None:
        Keyboard.press('v')

    def loot(self, coordinates: Coordinate) -> None:
        Keyboard.key_down('shift')
        self.mouse.use_right_button(coordinates)
        Keyboard.key_up('shift')

    def chase_opponent(self) -> None:
        Keyboard.press('g')

    def not_chase_opponent(self) -> None:
        Keyboard.press('g')

    # MOVEMENT

    def position(self, frame: np.array) -> Position:
        return Position.check(frame)

    def move(self, command: MoveCommand) -> None:
        Keyboard.press(command.key)
