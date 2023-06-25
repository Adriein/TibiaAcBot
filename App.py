from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage.Shared.Screen import Screen
from ScreenAnalizerPackage.Stats.Stat import Stat
from CaveBot.CaveBot import CaveBot
from CaveBot.AutoTrainner import AutoTrainner
from dotenv import load_dotenv
import argparse


class TibiaAcBot:
    @staticmethod
    def init():
        try:
            TibiaAcBot.setup_global()

            training_mode = TibiaAcBot.collect_program_arguments()

            TibiaAcBotLogger.info('Started...')
            TibiaAcBotLogger.info('Press Ctrl+C to stop the execution')

            if training_mode:
                TibiaAcBotLogger.info('Started in train mode')

                AutoTrainner().train()

                raise SystemExit

            TibiaAcBotLogger.info('Started in cave bot mode')

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

    @staticmethod
    def collect_program_arguments() -> bool:
        TibiaAcBotLogger.info('Collecting program arguments...')

        parser = argparse.ArgumentParser()

        parser.add_argument('--train', action="store_true", help='Indicate that program should start in training mode')

        if parser.parse_args() and parser.parse_args().train:
            return True

        return False


TibiaAcBot().init()
