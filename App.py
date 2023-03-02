import time
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import HitPoint


class TibiaAcBot:
    def init(self):
        try:
            TibiaAcBotLogger.log('Started...')
            TibiaAcBotLogger.log('Press Ctrl+C to stop the execution')

            while True:
                time.sleep(3)
                TibiaAcBotLogger.log('Listening...')

                hp = HitPoint()
                hp.get()
        except KeyboardInterrupt:
            TibiaAcBotLogger.log('\n')
            TibiaAcBotLogger.log('Graceful shutdown')


app = TibiaAcBot()

app.init()
