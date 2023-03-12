import time
from LoggerPackage import Logger as TibiaAcBotLogger
from CaveBot.Player import Player

import pyautogui


class TibiaAcBot:
    @staticmethod
    def init():
        try:
            TibiaAcBotLogger.info('Started...')
            TibiaAcBotLogger.info('Press Ctrl+C to stop the execution')

            while True:
                time.sleep(3)
                TibiaAcBotLogger.info('Listening...')
                # print(pyautogui.position())
                player = Player.create()

                player.health()
                player.mana()
        except KeyboardInterrupt:
            TibiaAcBotLogger.info('Graceful shutdown')
            raise SystemExit
        except Exception as error:
            TibiaAcBotLogger.error(str(error))
            raise SystemExit from error


TibiaAcBot().init()
