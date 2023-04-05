import numpy
import cv2


class Cv2File:
    @staticmethod
    def load_image(path: str, grey_scale=True) -> numpy.ndarray:
        if grey_scale:
            return numpy.array(cv2.imread(path, cv2.IMREAD_GRAYSCALE), dtype=numpy.uint8)

        return numpy.array(cv2.imread(path), dtype=numpy.uint8)
