from uuid import UUID


class Tile:
    def __init__(self, id: UUID, x: int, y: int, z: int):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

        self.adjacent_tiles = []

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.id == other.id and self.x == other.x and self.y == other.y and self.z == other.z

        return False

    def __str__(self):
        return f'Tile(x={self.x}, y={self.y}, z={self.z})'

    def add_adjacent_tile(self, node: 'Tile'):
        self.adjacent_tiles.append(node)
