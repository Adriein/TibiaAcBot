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
        frame_queue1 = Queue()

        walking_event = Event()
        combat_event = Event()

        while True:
            frame = WindowCapturer.start()

            frame_queue.put(frame)
            frame_queue1.put(frame)

            # attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(frame_queue, walking_event, combat_event))

            loot_thread = Thread(daemon=True, target=auto_loot.loot, args=(frame_queue1, walking_event, combat_event))

            # attack_thread.start()

            loot_thread.start()

             # attack_thread.join()
            loot_thread.join()

            cv2.imshow("Computer Vision", frame)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
