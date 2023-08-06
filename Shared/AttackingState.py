from CaveBot import Player
from ScreenAnalizerPackage import Coordinate
from Shared.BotState import BotState


class AttackingState(BotState):

    def __init__(self, player: Player) -> None:
        self.player = player
        super().__init__()

    def attack(self) -> None:
        self.player.attack()

    def walk(self) -> None:
        pass

    def heal(self) -> None:
        self.player.heal()

    def eat(self) -> None:
        self.player.eat()

    def use(self) -> None:
        pass

    def loot(self, coordinates: Coordinate) -> None:
        self.player.loot(coordinates)
