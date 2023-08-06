from CaveBot import Player
from Shared.AttackingState import AttackingState
from Shared.BotState import BotState
from collections import OrderedDict

from Shared.Task import Task


class Context:
    ATTACK = 'Attack'
    WALK = 'Walk'
    HEAL = 'Heal'
    EAT = 'Eat'
    LOOT = 'Loot'

    def __init__(self, player: Player, state: BotState) -> None:
        self.state = state
        self.tasks = OrderedDict([
            ('Attack', Task(self.ATTACK, AttackingState(player)))
        ])

    def getTask(self, task_name) -> Task:
        return self.tasks.get(task_name)
