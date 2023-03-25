import time
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage.Shared.Screen import Screen
from ScreenAnalizerPackage.Stats.Stat import Stat
from CaveBot.CaveBot import CaveBot
from dotenv import load_dotenv


class TibiaAcBot:
    @staticmethod
    def init():
        try:
            TibiaAcBot.setup_global()

            TibiaAcBotLogger.info('Started...')
            TibiaAcBotLogger.info('Press Ctrl+C to stop the execution')

            TibiaAcBotLogger.info('Listening...')

            cave_bot = CaveBot()

            cave_bot.start()

        except KeyboardInterrupt:
            TibiaAcBotLogger.info('Graceful shutdown')
            raise SystemExit
        except Exception as error:
            TibiaAcBotLogger.error(str(error), error)
            raise SystemExit from error

    @staticmethod
    def setup_global() -> None:
        TibiaAcBotLogger.info('Setting env...')

        load_dotenv()

        Screen.setup_global_variables()
        Stat.setup_global_variables()


TibiaAcBot().init()
