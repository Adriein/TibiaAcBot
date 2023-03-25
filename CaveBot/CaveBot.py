from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from threading import Thread
import time


class CaveBot:
    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        health_thread = Thread(daemon=True, target=player.watch_health).start()
        mana_thread = Thread(daemon=True, target=player.watch_mana).start()

        while True:
            time.sleep(10)
            print('moving north')
            #player.move_north()
