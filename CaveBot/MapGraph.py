from .Edge import Edge
from .Tile import Tile


class MapGraph:
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0

    def add_node(self, node: Tile):
        self.num_nodes += 1
        self.nodes[str(node.id)] = node

        return self

    def add_edge(self, edge: Edge):
        if edge.src not in self.nodes:
            self.add_node(edge.src)
        if edge.destination not in self.nodes:
            self.add_node(edge.destination)

        self.nodes[str(edge.src.id)].add_adjacent_tile(edge.destination, edge.distance_between)

    def __iter__(self):
        return iter(self.nodes.values())
