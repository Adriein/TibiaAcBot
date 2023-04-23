class MoveCommand:
    __DIRECTION_KEYBOARD_MAP = {
        "north": "w",
        "east": "d",
        "south": "s",
        "west": "a"
    }
    __BASE_0_RANGE_FIX = 1

    def __init__(self, steps: int, direction: str):
        self.steps = steps - self.__BASE_0_RANGE_FIX
        self.key = self.__DIRECTION_KEYBOARD_MAP.get(direction)
