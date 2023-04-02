class PositionError(Exception):
    def __init__(self, message: str):
        super(PositionError, self).__init__(f'Error guessing player position {message}')
