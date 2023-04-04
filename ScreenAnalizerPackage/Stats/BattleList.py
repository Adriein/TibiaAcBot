from ScreenAnalizerPackage import Scanner
from ScreenAnalizerPackage import ScreenRegion
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class BattleList:
    PIXELS_TO_GET_FULL_BATTLE_LIST_WIDGET_FROM_TITLE = 180
    @staticmethod
    def create(frame: np.array) -> 'BattleList':
        (left, top, width, height) = Scanner.player_battle_list_position(frame)

        return BattleList(ScreenRegion(left, top, width, height))

    def __init__(self, region: ScreenRegion):
        self.region = region

    def get_coordinates_of_nearest_creature(self, frame: np.array) -> tuple[int, int]:
        y = self.region.top + self.PIXELS_TO_GET_FULL_BATTLE_LIST_WIDGET_FROM_TITLE
        x = self.region.left

        battle_list_roi = frame[y:y + self.region.height, x:x + self.region.width]
        creature_template = Cv2File.load_image('Wiki/Ui/Battle/Mobs/mountain_troll.png')

        match = cv2.matchTemplate(battle_list_roi, creature_template, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        end_x = start_x + creature_template.shape[1]
        end_y = start_y + creature_template.shape[0]

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

            # draw the bounding box on the image
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 1)
        # show the output image
        cv2.imshow("Output", frame)
        cv2.waitKey(0)
        pass
