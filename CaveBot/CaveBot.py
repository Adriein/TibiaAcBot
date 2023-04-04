from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from .AutoAttack import AutoAttack
from threading import Thread
import time


class CaveBot:
    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()
        AutoAttack.start()
        raise Exception('controlled exception')
        # Thread(daemon=True, target=player.watch_health).start()
        # Thread(daemon=True, target=player.watch_mana).start()

        while True:
            time.sleep(2)

            player.position()
