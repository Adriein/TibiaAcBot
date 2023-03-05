import numpy
import cv2


class Cv2File:
    @staticmethod
    def load_image(path: str) -> numpy.ndarray:
        return numpy.array(cv2.imread(path, cv2.IMREAD_GRAYSCALE), dtype=numpy.uint8)
