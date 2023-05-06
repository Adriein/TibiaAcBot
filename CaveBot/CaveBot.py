from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer
import cv2
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from .Script import Script
from .PathFinder import PathFinder
from threading import Thread, Event
from queue import Queue


class CaveBot:

    def __start_walking(self, cave_bot_script: Script, walking_event: Event):
        walking_event.set()

        walk_thread = Thread(daemon=True, target=cave_bot_script.start, args=(walking_event,))

        walk_thread.start()

    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        walking_event = Event()
        combat_event = Event()

        # Thread(daemon=True, target=player.watch_mana).start()

        cave_bot_script = Script.load('Wiki/Script/Rookgard/mountain_troll_salamander_script.json', player)

        auto_attack = AutoAttack(player, walking_event, combat_event, cave_bot_script.creatures)

        auto_loot = AutoLoot(player, walking_event, combat_event)

        # self.__start_walking(cave_bot_script, walking_event)

        path_finder = PathFinder()

        while True:
            frame = WindowCapturer.start()

            path_finder.where_am_i(frame)

            health_thread = Thread(daemon=True, target=player.watch_health, args=(frame,))

            attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(frame,))

            loot_thread = Thread(daemon=True, target=auto_loot.loot, args=(frame,))

            health_thread.start()

            attack_thread.start()

            loot_thread.start()

            health_thread.join()
            attack_thread.join()
            loot_thread.join()

            # cv2.imshow("Computer Vision", frame)

            # if cv2.waitKey(1) == ord('q'):
            #  cv2.destroyAllWindows()
            # break
