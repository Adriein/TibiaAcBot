class NoCreatureFound(Exception):
    def __init__(self):
        super(NoCreatureFound, self).__init__("The battle list is empty")
