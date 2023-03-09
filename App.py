import time
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import HitPoint
from ScreenAnalizerPackage import Mana
from CaveBot.Player import Player

import pyautogui


class TibiaAcBot:
    def init(self):
        try:
            TibiaAcBotLogger.info('Started...')
            TibiaAcBotLogger.info('Press Ctrl+C to stop the execution')

            while True:
                time.sleep(3)
                TibiaAcBotLogger.info('Listening...')
                # print(pyautogui.position())
                player = Player.create()

                player.health()
        except KeyboardInterrupt:
            TibiaAcBotLogger.info('Graceful shutdown')
            raise SystemExit


app = TibiaAcBot()

app.init()
