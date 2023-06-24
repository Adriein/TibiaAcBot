from .Player import Player
from LoggerPackage import Logger as TibiaAcBotLogger
from ScreenAnalizerPackage import Screen
from .AutoAttack import AutoAttack
from .AutoLoot import AutoLoot
from .AutoWalk import AutoWalk
from .AutoHealer import AutoHealer
from .Script import Script
from threading import Thread, Event


class AutoTrainner:
    TibiaAcBotLogger.info('CaveBot starting')

    player = Player.create()

    walking_event = Event()
    combat_event = Event()

    cave_bot_script = Script.load('Wiki/Script/Thais/thais_wasp.json')

    auto_loot = AutoLoot(player, Screen.GAME_WINDOW)

    auto_attack = AutoAttack(auto_loot, player, walking_event, combat_event, cave_bot_script.creatures)

    auto_healer = AutoHealer(player, combat_event)

    attack_thread = Thread(daemon=True, target=auto_attack.attack)

    health_thread = Thread(daemon=True, target=auto_healer.heal)

    attack_thread.start()

    health_thread.start()

    while True:
        pass
