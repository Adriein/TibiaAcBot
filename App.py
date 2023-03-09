import time
from LoggerPackage import Logger as TibiaAcBotLogger
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
                player.mana()
        except KeyboardInterrupt:
            TibiaAcBotLogger.info('Graceful shutdown')
            raise SystemExit
        except Exception as fatal:
            TibiaAcBotLogger.error(f'Fatal Exception: {str(fatal)}')
            raise SystemExit


app = TibiaAcBot()

app.init()
