from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Error.NoCreatureFound import NoCreatureFound
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class BattleList:
    BATTLE_LIST_WIDGET_HEIGHT = 180

    @staticmethod
    def create(frame: np.array) -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position(frame)

        height = top + height + BattleList.BATTLE_LIST_WIDGET_HEIGHT

        return BattleList(ScreenRegion(left, top, width, height))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def find_enemies(self, frame: np.array) -> list[ScreenRegion]:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        battle_list_in_frame_y = self.region.top
        battle_list_in_frame_x = self.region.left

        battle_list_in_frame_width = battle_list_in_frame_x + self.region.width
        battle_list_in_frame_height = battle_list_in_frame_y + self.region.height

        battle_list_roi = frame[battle_list_in_frame_y: battle_list_in_frame_height, battle_list_in_frame_x: battle_list_in_frame_width]

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

                frame_creature_position_x = battle_list_in_frame_x + nearest_creature_battle_list_roi_x
                frame_creature_position_y = battle_list_in_frame_y + nearest_creature_battle_list_roi_y
                frame_creature_width = frame_creature_position_x + creature_template_width
                frame_creature_height = frame_creature_position_y + creature_template_height

                # click_point_x = frame_creature_position_x + int(creature_template_width/2)
                # click_point_y = frame_creature_position_y + int(creature_template_height/2)

                results.append(
                    ScreenRegion(
                        frame_creature_position_x,
                        frame_creature_position_y,
                        frame_creature_width,
                        frame_creature_height
                    )
                )

            return results

        raise NoCreatureFound()

    def is_nearest_creature_attacked(self, frame: np.array, nearest_creature_region: ScreenRegion) -> bool:
        start_x = nearest_creature_region.left
        start_y = nearest_creature_region.top
        end_x = nearest_creature_region.width
        end_y = nearest_creature_region.height


        battle_list_attack_template = Cv2File.load_image(
            'Wiki/Ui/Battle/Mobs/MountainTroll/mountain_troll_attacked.png',
            grey_scale=False
        )

        template_width, *_ = battle_list_attack_template.shape

        battle_list_roi = frame[start_y: end_y, start_x - 10: start_x]

        # show the output image
        cv2.imshow("Output", battle_list_roi)
        cv2.waitKey(0)

        raise Exception

        battle_list_roi_hsv = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])

        mask = cv2.inRange(battle_list_roi_hsv, lower_red, upper_red)

        if np.any(mask == 255):
            print('Red color is present in the image.')
        else:
            print('Red color is not present in the image.')




