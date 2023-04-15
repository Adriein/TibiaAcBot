from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer
import cv2
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from threading import Thread
from queue import Queue
from threading import Event


class CaveBot:
    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        # Thread(daemon=True, target=player.watch_health).start()
        # Thread(daemon=True, target=player.watch_mana).start()

        auto_attack = AutoAttack.start(player)

        auto_loot = AutoLoot(player)

        frame_queue = Queue()

        event = Event()

        attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(frame_queue, event))

        loot_thread = Thread(daemon=True, target=auto_loot.loot, args=(frame_queue, event))

        while True:
            frame = WindowCapturer.start()

            frame_queue.put(frame)

            attack_thread.start()

            loot_thread.start()

            attack_thread.join()
            loot_thread.join()

            cv2.imshow("Computer Vision", frame)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
