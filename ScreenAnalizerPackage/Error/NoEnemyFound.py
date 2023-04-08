class NoEnemyFound(Exception):
    def __init__(self):
        super(NoEnemyFound, self).__init__("The battle list is empty")
