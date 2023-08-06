from abc import ABC, abstractmethod

from ScreenAnalizerPackage import Coordinate


class BotState(ABC):
    @abstractmethod
    def attack(self) -> None:
        pass

    @abstractmethod
    def walk(self) -> None:
        pass

    @abstractmethod
    def heal(self) -> None:
        pass

    @abstractmethod
    def eat(self) -> None:
        pass

    @abstractmethod
    def use(self) -> None:
        pass

    @abstractmethod
    def loot(self, coordinate: Coordinate) -> None:
        pass
