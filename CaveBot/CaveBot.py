from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer
import cv2
from .AutoAttack import AutoAttack
from threading import Thread
import time


class CaveBot:
    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        # Thread(daemon=True, target=player.watch_health).start()
        # Thread(daemon=True, target=player.watch_mana).start()

        while True:
            capture = WindowCapturer.start()

            cv2.imshow("Computer Vision", capture)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break



