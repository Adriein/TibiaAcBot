from LoggerPackage import Logger as TibiaAcBotLogger


class AutoHealer:
    HIT_POINT_THRESHOLD = 20
    MANA_THRESHOLD = 5

    def heal(self) -> None:
        TibiaAcBotLogger.debug(f'player healed')

    def have_to_be_healed(self, hp: int) -> bool:
        return hp <= self.HIT_POINT_THRESHOLD

    def use_mana_potion(self) -> None:
        TibiaAcBotLogger.debug(f'player used mana potion')

    def need_mana(self, mana: int) -> bool:
        return mana <= self.MANA_THRESHOLD
