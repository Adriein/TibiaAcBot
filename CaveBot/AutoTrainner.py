from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from .TrainingAutoAttack import TrainingAutoAttack
from .AutoHealer import AutoHealer
from .Script import Script
from threading import Thread, Event
import time
import random


class AutoTrainner:
    def __init__(self):
        pass

    def train(self) -> None:
        TibiaAcBotLogger.info('AutoTraining starting')

        # player = Player.create()

        # combat_event = Event()

        # training_script = Script.load('Wiki/Script/Training/training.json')

        # auto_attack = TrainingAutoAttack(player, training_script.creatures, combat_event)

        # attack_thread = Thread(daemon=True, target=auto_attack.train)

        # attack_thread.start()

        # while True:
        # pass
        while True:
            # Generate a random sleep time between 5 and 15 seconds
            sleep_duration = generate_random_sleep_time()

            # Sleep for the randomly generated time
            time.sleep(sleep_duration * 60)

            # Log a message to the console
            TibiaAcBotLogger.info(f'Slept for {sleep_duration} seconds. Eating and casting spells')
            player = Player.create()
            player.eat()
            player.heal()

    def generate_random_sleep_time(self):
        return random.randint(1, 15)
