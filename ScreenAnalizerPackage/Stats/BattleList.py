from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Error.NoEnemyFound import NoEnemyFound
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class BattleList:
    BATTLE_LIST_WIDGET_HEIGHT = 180

    @staticmethod
    def create(frame: np.array) -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position(frame)

        start_x = left
        end_x = left + width
        start_y = top
        end_y = top + height + BattleList.BATTLE_LIST_WIDGET_HEIGHT

        return BattleList(ScreenRegion(start_x, end_x, start_y, end_y))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def find_enemies(self, frame: np.array) -> list[ScreenRegion]:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        battle_list_roi = frame[self.region.start_y: self.region.end_y, self.region.start_x: self.region.end_x]

        creature_template = Cv2File.load_image('Wiki/Ui/Battle/Mobs/MountainTroll/mountain_troll_label.png')

        match = cv2.matchTemplate(battle_list_roi, creature_template, cv2.TM_CCOEFF_NORMED)

        # match_locations = (y_match_coords, x_match_coords) >= similarity more than threshold
        match_locations = np.where(match >= 0.9)

        # paired_match_locations = [(x, y), (x, y)]
        paired_match_locations = list(zip(*match_locations[::-1]))

        ordered_match_locations = sorted(paired_match_locations, key=lambda pair: pair[1], reverse=False)

        if ordered_match_locations:
            results = list()

            for (nearest_creature_battle_list_roi_x, nearest_creature_battle_list_roi_y) in ordered_match_locations:
                creature_template_height, creature_template_width = creature_template.shape

                frame_creature_position_start_x = self.region.start_x + nearest_creature_battle_list_roi_x
                frame_creature_position_start_y = self.region.start_y + nearest_creature_battle_list_roi_y
                frame_creature_end_x = frame_creature_position_start_x + creature_template_width
                frame_creature_end_y = frame_creature_position_start_y + creature_template_height

                battle_list_position = ScreenRegion(
                    frame_creature_position_start_x,
                    frame_creature_end_x,
                    frame_creature_position_start_y,
                    frame_creature_end_y
                )

                results.append(battle_list_position)

            return results

        raise NoEnemyFound()

    def is_nearest_enemy_attacked(self, frame: np.array, nearest_creature_region: ScreenRegion) -> bool:
        start_x = nearest_creature_region.start_x
        start_y = nearest_creature_region.start_y
        end_y = nearest_creature_region.end_y

        battle_list_attack_template = Cv2File.load_image(
            'Wiki/Ui/Battle/Mobs/MountainTroll/mountain_troll_attacked.png',
            grey_scale=False
        )

        template_width, *_ = battle_list_attack_template.shape

        battle_list_roi = frame[start_y: end_y, start_x - 4: start_x]

        battle_list_roi_hsv = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2HSV)

        # create a red color range
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])

        # check if red color is present in the roi image
        mask = cv2.inRange(battle_list_roi_hsv, lower_red, upper_red)

        return np.any(mask == 255)
