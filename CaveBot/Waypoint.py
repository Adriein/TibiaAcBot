class Waypoint:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'x={self.x} y={self.y} z={self.z}'

    def __eq__(self, other):
        if isinstance(other, Waypoint):
            return self.x == other.x and self.y == other.y and self.z == other.z

        return False

    def to_string(self) -> str:
        return f'{self.x},{self.y},{self.z}'
