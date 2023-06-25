from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from .TrainingAutoAttack import TrainingAutoAttack
from .AutoHealer import AutoHealer
from .Script import Script
from threading import Thread, Event


class AutoTrainner:
    def train(self) -> None:
        TibiaAcBotLogger.info('AutoTraining starting')

        player = Player.create()

        combat_event = Event()

        training_script = Script.load('Wiki/Script/Training/training.json')

        auto_attack = TrainingAutoAttack(player, training_script.creatures, combat_event)

        attack_thread = Thread(daemon=True, target=auto_attack.train)

        attack_thread.start()

        while True:
            pass
