from ScreenAnalizerPackage import BattleList


class AutoAttack:
    @staticmethod
    def start() -> None:
        battle_list = BattleList.create()

        battle_list.get_coordinates_of_nearest_creature()
