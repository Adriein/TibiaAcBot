from .Tile import Tile


class Edge:
    def __init__(self, src: Tile, destination: Tile, distance_between: float):
        self.src = src
        self.destination = destination
        self.distance_between = distance_between
