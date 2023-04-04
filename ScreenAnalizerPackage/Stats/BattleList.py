from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
import pyautogui


class BattleList:
    @staticmethod
    def create() -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position()

        return BattleList(ScreenRegion(left, top, width, height))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def get_coordinates_of_nearest_creature(self) -> tuple[int, int]:
        results = pyautogui.locateAllOnScreen(
            'Wiki/Ui/Battle/Mobs/mountain_troll.png',
            grayscale=True,
            region=(self.region.left, self.region.top, self.region.width, self.region.height + 200)
        )
        print(self.region)
        print(results)

        for result in results:
            print(result)
