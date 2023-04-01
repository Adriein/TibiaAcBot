from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from threading import Thread
import time


class CaveBot:
    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        Thread(daemon=True, target=player.watch_health).start()
        Thread(daemon=True, target=player.watch_mana).start()

        while True:
            time.sleep(2)

            player.position()
