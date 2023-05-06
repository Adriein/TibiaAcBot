import numpy as np
from ScreenAnalizerPackage import Scanner


class PathFinder:
    def where_am_i(self, frame: np.array):
        Scanner.mini_map_position(frame)