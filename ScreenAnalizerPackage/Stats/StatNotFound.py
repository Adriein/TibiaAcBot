class StatNotFound(Exception):
    def __init__(self):
        super(StatNotFound, self).__init__("Stat not found fatal error")
