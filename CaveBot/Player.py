from ScreenAnalizerPackage import HitPoint
from ScreenAnalizerPackage import Mana
from LoggerPackage import Logger


class Player:
    @staticmethod
    def create() -> 'Player':
        return Player(HitPoint(), Mana())

    def __init__(self, hp: HitPoint, mana_bar: Mana):
        self.hp = hp
        self.mana_bar = mana_bar

    def health(self) -> int:
        player_health = self.hp.get()
        Logger.debug(f'health: {player_health}')

        return player_health

    def mana(self) -> int:
        player_mana = self.mana_bar.get()
        Logger.debug(f'mana: {player_mana}')
        return player_mana
