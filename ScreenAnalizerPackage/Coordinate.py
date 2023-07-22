from ScreenAnalizerPackage.ScreenRegion import ScreenRegion


class Coordinate:
    @staticmethod
    def from_screen_region(region: ScreenRegion):
        x = region.start_x + int((region.end_x - region.start_x) / 2)
        y = region.start_y + int((region.end_y - region.start_y) / 2)

        return Coordinate(x, y)

    @staticmethod
    def from_game_window_to_screen(coordinate: 'Coordinate'):
        screen_relative_x = int(coordinate.x * (1366 / 940))
        screen_relative_y = int(coordinate.y * (1366 / 940))

        return Coordinate(screen_relative_x, screen_relative_y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def equals(self, coordinate: 'Coordinate') -> bool:
        if not isinstance(coordinate, Coordinate):
            return False

        if not coordinate.x == self.x or not coordinate.y == self.y:
            return False

        return True

    def __str__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

