from ScreenAnalizerPackage import ScreenRegion
from ScreenAnalizerPackage import Coordinate


class Enemy:
    def __init__(self, name: str, runner: bool, loot: bool, position: ScreenRegion):
        self.name = name
        self.runner = runner
        self.loot = loot
        self.position = position

    def click_coords(self) -> Coordinate:
        return Coordinate.from_screen_region(self.position)
