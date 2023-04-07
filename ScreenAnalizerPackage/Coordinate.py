from ScreenAnalizerPackage.ScreenRegion import ScreenRegion


class Coordinate:
    @staticmethod
    def from_screen_region(region: ScreenRegion):
        x = int((region.start_x - region.end_x) / 2)
        y = int((region.start_y - region.end_y) / 2)

        return Coordinate(x, y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
