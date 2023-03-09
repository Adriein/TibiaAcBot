from ScreenAnalizerPackage import HitPoint
from ScreenAnalizerPackage import Mana
from LoggerPackage import Logger


class Player:
    @staticmethod
    def create() -> 'Player':
        hp = HitPoint()
        mana = Mana()

        return Player(hp, mana)

    def __init__(self, hp: HitPoint, mana: Mana):
        self.hp = hp
        self.mana = mana

    def health(self) -> int:
        player_health = self.hp.get()
        Logger.debug(f'health: {player_health}')

        return player_health

    def mana(self) -> int:
        player_mana = self.mana.get()
        Logger.debug(f'mana: {player_mana}')
        return player_mana
