class ScreenRegion:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @staticmethod
    def from_box(box) -> 'ScreenRegion':
        return ScreenRegion(box.left, box.top, box.width, box.height)
