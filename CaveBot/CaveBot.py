from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import Screen
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
        cave_bot_script = Script.load('Wiki/Script/Venore/swampling_cave.json')

        auto_loot = AutoLoot(player, Screen.GAME_WINDOW)

        auto_walk = AutoWalk(cave_bot_script, player, walking_event)

        auto_attack = AutoAttack(auto_loot, player, walking_event, combat_event, cave_bot_script.creatures)

        auto_healer = AutoHealer(player, combat_event)

        attack_thread = Thread(daemon=True, target=auto_attack.attack)

        walk_thread = Thread(daemon=True, target=auto_walk.start)

        health_thread = Thread(daemon=True, target=auto_healer.heal)

        attack_thread.start()

        health_thread.start()

        walk_thread.start()

        walking_event.set()

