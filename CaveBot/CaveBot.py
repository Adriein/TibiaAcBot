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

        attack_frame_queue = Queue()
        loot_frame_queue = Queue()

        walking_event = Event()
        combat_event = Event()

        while True:
            frame = WindowCapturer.start()

            attack_frame_queue.put(frame)
            loot_frame_queue.put(frame)

            attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(attack_frame_queue, walking_event, combat_event))

            loot_thread = Thread(daemon=True, target=auto_loot.loot, args=(loot_frame_queue, walking_event, combat_event))

            attack_thread.start()

            loot_thread.start()

            attack_thread.join()
            loot_thread.join()

            cv2.imshow("Computer Vision", frame)

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
