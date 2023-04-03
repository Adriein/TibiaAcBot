from ScreenAnalizerPackage import Position
from ScreenAnalizerPackage import BattleList


class AutoAttack:
    @staticmethod
    def start(player_position: Position) -> None:
        battle_list = BattleList.create()
