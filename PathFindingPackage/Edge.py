from PathFindingPackage import CoordinateNode


class Edge:
    def __init__(self, src: CoordinateNode, destination: CoordinateNode, distance_between: float):
        self.src = src
        self.destination = destination
        self.distance_between = distance_between
