class Waypoint:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'x={self.x} y={self.y} z={self.z}'
