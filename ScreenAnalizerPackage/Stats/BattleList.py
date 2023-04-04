from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion


class BattleList:
    @staticmethod
    def create() -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position()

        return BattleList(ScreenRegion(left, top, width, height))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def get_coordinates_of_nearest_creature(self, frame) -> tuple[int, int]:
        pass