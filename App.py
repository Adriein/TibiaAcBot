import time
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import HitPoint
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
                hp = HitPoint()
                print(hp.get())
        except KeyboardInterrupt:
            TibiaAcBotLogger.info('Graceful shutdown')
            raise SystemExit


app = TibiaAcBot()

app.init()
