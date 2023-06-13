from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import WindowCapturer
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from .AutoWalk import AutoWalk
from .AutoHealer import AutoHealer
from .Script import Script
from threading import Thread, Event


class CaveBot:

    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        walking_event = Event()
        combat_event = Event()

        # Thread(daemon=True, target=player.watch_mana).start()
        cave_bot_script = Script.load('Wiki/Script/Thais/thais_wasp_first_floor.json')

        auto_walk = AutoWalk(cave_bot_script, player)

        auto_attack = AutoAttack(player, walking_event, combat_event, cave_bot_script.creatures)

        auto_loot = AutoLoot(player, walking_event, combat_event)

        auto_healer = AutoHealer(player)

        walk_thread = Thread(daemon=True, target=auto_walk.start, args=(walking_event,))

        health_thread = Thread(daemon=True, target=auto_healer.heal, args=(walking_event,))

        health_thread.start()

        walk_thread.start()

        walking_event.set()

        while True:
            frame = WindowCapturer.start()

            attack_thread = Thread(daemon=True, target=auto_attack.attack, args=(frame,))

            loot_thread = Thread(daemon=True, target=auto_loot.loot)

            attack_thread.start()
            loot_thread.start()

            attack_thread.join()
            loot_thread.join()

            # cv2.imshow("Computer Vision", frame)

            # if cv2.waitKey(1) == ord('q'):
            #  cv2.destroyAllWindows()
            # break
