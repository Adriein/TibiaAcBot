from Shared.BotState import BotState


class Task:
    def __init__(self, name, state: BotState) -> None:
        self.name = name
        self.state = state
