from ScreenAnalizerPackage.ScreenRegion import ScreenRegion


class Coordinate:
    @staticmethod
    def from_screen_region(region: ScreenRegion):
        x = region.start_x + int((region.end_x - region.start_x) / 2)
        y = region.start_y + int((region.end_y - region.start_y) / 2)

        return Coordinate(x, y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def equals(self, coordinate: 'Coordinate') -> bool:
        if not isinstance(coordinate, Coordinate):
            return False

        if not coordinate.x == self.x or not coordinate.y == self.y:
            print('incoming coordinate')
            print(coordinate.x)
            print('actual coordinate')
            print(self.x)
            print('----------------------------------------------------------------------')
            return False

        return True

