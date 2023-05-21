class MoveCommand:
    __DIRECTION_KEYBOARD_MAP = {
        "north": "w",
        "east": "d",
        "south": "s",
        "west": "a"
    }
    __BASE_0_RANGE_FIX = 1

    def __init__(self, steps: int, direction: str):
        self.steps = steps
        self.key = self.__DIRECTION_KEYBOARD_MAP.get(direction)

    def __str__(self):
        return f'key={self.key}'
