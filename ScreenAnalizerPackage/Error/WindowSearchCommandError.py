class WindowSearchCommandError(Exception):
    def __init__(self, window_name: str):
        super(WindowSearchCommandError, self).__init__(f'Error executing xdotool search --name {window_name}')