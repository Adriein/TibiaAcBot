from ScreenAnalizerPackage import Position

class AutoAttack:
    @staticmethod
    def start(player_position: Position) -> None:
        auto_attack_zone_start_x = player_position.start_x - 40
        auto_attack_zone_start_y = player_position.start_y - 40

        auto_attack_zone_end_x = player_position.end_x + 40
        auto_attack_zone_end_y = player_position.end_y - 40



