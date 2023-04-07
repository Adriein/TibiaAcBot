from ScreenAnalizerPackage.ScreenRegion import ScreenRegion


class Coordinate:
    @staticmethod
    def from_screen_region(region: ScreenRegion):
        x = region.left + int(region.width / 2)
        y = region.top + int(region.height / 2)

        return Coordinate(x, y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
