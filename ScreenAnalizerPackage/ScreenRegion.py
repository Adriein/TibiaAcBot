class ScreenRegion:
    def __init__(self, start_x: int, end_x: int, start_y: int, end_y: int):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

    def __str__(self):
        return f'ScreenRegion(start_x={self.start_x}, end_x={self.end_x}, start_y={self.start_y}, end_y={self.end_y})'
