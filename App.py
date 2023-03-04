import time
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import HitPoint
import pyautogui

class TibiaAcBot:
    def init(self):
        try:
            TibiaAcBotLogger.log('Started...')
            TibiaAcBotLogger.log('Press Ctrl+C to stop the execution')

            while True:
                time.sleep(3)
                TibiaAcBotLogger.log('Listening...')
                #print(pyautogui.position())
                hp = HitPoint()
                hp.get()
        except KeyboardInterrupt:
            TibiaAcBotLogger.log('Graceful shutdown')
            raise SystemExit


app = TibiaAcBot()

app.init()
