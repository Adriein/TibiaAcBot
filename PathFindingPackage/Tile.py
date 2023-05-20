import uuid
from uuid import UUID
from .Waypoint import Waypoint


class Tile:
    @staticmethod
    def build(waypoint: Waypoint) -> 'Tile':

        return Tile(uuid.uuid4(), waypoint)

    def __init__(self, id: UUID, waypoint: Waypoint):
        self.id = id
        self.waypoint = waypoint

        self.g_score = 1  # Cost from start node
        self.h_score = 0  # Heuristic score
        self.f_score = float('inf')  # Total score (g_score + h_score)
        self.parent = None  # Parent node

        self.adjacent_tiles: list[Tile] = []

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.waypoint.x == other.waypoint.x and self.waypoint.y == other.waypoint.y and self.waypoint.z == other.waypoint.z

        return False

    def __str__(self):
        return f'Tile(x={self.waypoint.x}, y={self.waypoint.y}, z={self.waypoint.z})'

    def set_parent(self, node: 'Tile'):
        self.parent = node

    def add_adjacent_tile(self, tile: 'Tile') -> None:
        self.adjacent_tiles.append(tile)

    def calculate_cost(self, destination: Waypoint):
        self.h_score = self.__calculate_distance_between_two_points(destination)

        self.f_score = self.h_score + self.g_score

    def __calculate_distance_between_two_points(self, destination: Waypoint) -> float:
        return ((destination.x - self.waypoint.x) ** 2 + (destination.y - self.waypoint.y) ** 2) ** 0.5
