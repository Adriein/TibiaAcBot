from PathFindingPackage.CoordinateNode import CoordinateNode


class MapGraph:
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0

    def add_node(self, id: str):
        self.num_nodes += 1
        new_node = CoordinateNode(id)
        self.nodes[id] = new_node
        return new_node

    def add_edge(self, src, dest, weight=0):
        if src not in self.nodes:
            self.add_node(src)
        if dest not in self.nodes:
            self.add_node(dest)
        self.nodes[src].add_neighbor(self.nodes[dest], weight)

    def __iter__(self):
        return iter(self.nodes.values())
