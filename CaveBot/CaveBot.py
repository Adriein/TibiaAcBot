from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import Screen
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from .AutoWalk import AutoWalk
from .Script import Script
from threading import Thread, Event


class CaveBot:

    def start(self):
        TibiaAcBotLogger.info('CaveBot starting')

        player = Player.create()

        # Thread(daemon=True, target=player.watch_mana).start()
        cave_bot_script = Script.load('Wiki/Script/Thais/thais_wasp.json')
        # cave_bot_script = Script.load('Wiki/Script/Venore/swamp_troll_cave.json')
        # cave_bot_script = Script.load('Wiki/Script/Venore/swampling_cave_floor_10.json')

        while True:
            pass

