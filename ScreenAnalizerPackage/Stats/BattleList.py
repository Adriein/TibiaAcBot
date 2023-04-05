from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class BattleList:
    BATTLE_LIST_WIDGET_HEIGHT = 180

    @staticmethod
    def create(frame: np.array) -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position(frame)

        return BattleList(ScreenRegion(left, top, width, height))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def get_coordinates_of_nearest_creature(self, frame: np.array) -> tuple[int, int]:
        battle_list_in_frame_y = self.region.top
        battle_list_in_frame_x = self.region.left

        battle_list_in_frame_width = battle_list_in_frame_x + self.region.width
        battle_list_in_frame_height = battle_list_in_frame_y + self.region.height + self.BATTLE_LIST_WIDGET_HEIGHT

        battle_list_roi = frame[battle_list_in_frame_y: battle_list_in_frame_height, battle_list_in_frame_x: battle_list_in_frame_width]

        creature_template = Cv2File.load_image('Wiki/Ui/Battle/Mobs/mountain_troll.png')

        match = cv2.matchTemplate(battle_list_roi, creature_template, cv2.TM_CCOEFF_NORMED)

        # match_locations = (y_match_coords, x_match_coords) >= similarity more than threshold
        match_locations = np.where(match >= 0.9)

        # paired_match_locations = [(x, y), (x, y)]
        paired_match_locations = list(zip(*match_locations[::-1]))

        (creature_battle_list_roi_x, creature_battle_list_roi_y) = max_coordinates

        end_x = battle_list_in_frame_x + creature_battle_list_roi_x + creature_template.shape[1]
        end_y = battle_list_in_frame_y + creature_battle_list_roi_y + creature_template.shape[0]

        pass
