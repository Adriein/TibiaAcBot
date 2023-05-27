from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer, Screen
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from .Script import Script
from threading import Thread, Event
import cv2


class CaveBot:

    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        walking_event = Event()
        combat_event = Event()

        # Thread(daemon=True, target=player.watch_mana).start()

        cave_bot_script = Script.load('Wiki/Script/Rookgard/mountain_troll_salamander_script.json', player,
                                      walking_event)

        auto_attack = AutoAttack(player, walking_event, combat_event, cave_bot_script.creatures)

        auto_loot = AutoLoot(player, walking_event, combat_event)

        walking_event.set()

        while True:
            frame = WindowCapturer.start()

            screen_x = Screen.MONITOR.width / 2
            screen_y = Screen.MONITOR.height / 2
            print(screen_x)
            print(screen_y)
            if cv2.waitKey(1):
                cv2.destroyAllWindows()

            cv2.drawMarker(frame, (screen_x, screen_y), (255, 0, 255), cv2.MARKER_CROSS, cv2.LINE_4)
            cv2.imshow("Output", frame)
            cv2.waitKey(0)

            raise Exception


            walk_thread = Thread(daemon=True, target=cave_bot_script.start, args=(frame,))

            health_thread = Thread(daemon=True, target=player.watch_health, args=(frame,))

            attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(frame,))

            loot_thread = Thread(daemon=True, target=auto_loot.loot, args=(frame,))

            walk_thread.start()

            health_thread.start()

            attack_thread.start()

            loot_thread.start()

            walk_thread.join()
            health_thread.join()
            attack_thread.join()
            loot_thread.join()

            # cv2.imshow("Computer Vision", frame)

            # if cv2.waitKey(1) == ord('q'):
            #  cv2.destroyAllWindows()
            # break
