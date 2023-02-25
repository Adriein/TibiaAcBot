import pyautogui
import time
from LoggerPackage import Logger as TibiaAcBotLogger


class TibiaAcBot:
    def init(self):
        try:
            TibiaAcBotLogger.log('Started...')
            TibiaAcBotLogger.log('Press Ctrl+C to stop the execution')
            # pyautogui.screenshot('Screenshots/example.png')
            print(pyautogui.getAllWindows())

            while True:
                time.sleep(2)
                TibiaAcBotLogger.log('Listening...')

                capture = pyautogui.locateOnScreen('Screenshots/Stats/life_stats.png')
                print(pyautogui.position())
                print(capture)
        except KeyboardInterrupt:
            TibiaAcBotLogger.log('\n')
            TibiaAcBotLogger.log('Graceful shutdown')


app = TibiaAcBot()

app.init()
