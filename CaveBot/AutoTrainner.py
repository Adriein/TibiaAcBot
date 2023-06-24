from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from .TrainingAutoAttack import TrainingAutoAttack
from .AutoHealer import AutoHealer
from .Script import Script
from threading import Thread, Event


class AutoTrainner:
    TibiaAcBotLogger.info('CaveBot starting')

    player = Player.create()

    combat_event = Event()

    training_script = Script.load('Wiki/Script/Training/training.json')

    auto_attack = TrainingAutoAttack(player, training_script.creatures)

    auto_healer = AutoHealer(player, combat_event)

    attack_thread = Thread(daemon=True, target=auto_attack.train)

    health_thread = Thread(daemon=True, target=auto_healer.heal)

    attack_thread.start()

    health_thread.start()

    while True:
        pass
