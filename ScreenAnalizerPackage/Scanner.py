import cv2
import re
import pyautogui
from glob import glob
from ScreenAnalizerPackage.Error.ImageIsNotNumber import ImageIsNotNumber
from FilesystemPackage import Cv2File
import numpy as np


class Scanner:
    @staticmethod
    def ring_position(frame: np.array) -> tuple[int, int, int, int]:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        soul_anchor = Cv2File.load_image('Wiki/Ui/GameWindow/soul.png')

        match = cv2.matchTemplate(grey_scale_frame, soul_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = soul_anchor.shape

        return x, x + width, y, y + height
    @staticmethod
    def combat_stance_position(frame: np.array) -> tuple[int, int, int, int]:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        combat_stance_anchor = Cv2File.load_image('Wiki/Ui/Battle/combat_stance.png')

        match = cv2.matchTemplate(grey_scale_frame, combat_stance_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = combat_stance_anchor.shape

        frame_roi = frame[y:y + height + 20, x:x + width]

        hsv_image = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Window name in which image is displayed
        window_name = 'image'

        # Using cv2.imshow() method
        # Displaying the image
        cv2.imshow(window_name, hsv_image)

        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()

        return x, x + width, y, y + height

    @staticmethod
    def mini_map_position(frame: np.array) -> tuple[int, int, int, int]:
        mini_map_anchor = Cv2File.load_image('Wiki/Ui/Map/radar_anchor.png')

        match = cv2.matchTemplate(frame, mini_map_anchor, cv2.TM_CCOEFF_NORMED)

        [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        start_x = x - 117
        end_x = start_x + 106
        start_y = y - 50
        end_y = start_y + 109

        return start_x, end_x, start_y, end_y
    @staticmethod
    def player_battle_list_position(frame: np.array) -> tuple[int, int, int, int]:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        region = pyautogui.locate('Wiki/Ui/Battle/battle_list.png', grey_scale_frame, confidence=0.8, grayscale=True)

        return region.left, region.top, region.width, region.height

    @staticmethod
    def player_position(frame: np.ndarray, confidence: float) -> tuple[int, int, int, int, str]:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        player_position_templates = glob('Wiki/Player/Direction/*.png')

        start_x = 0
        start_y = 0

        position_direction = None

        for position_path in player_position_templates:
            position_template = Cv2File.load_image(position_path)

            match = cv2.matchTemplate(grey_scale_frame, position_template, cv2.TM_CCOEFF_NORMED)

            [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

            if Scanner.__ensure_confidence_threshold(confidence, max_coincidence):
                continue

            position_direction = re.search(r'(?<=/)\w+(?=\.)', position_path).group(0)

            (start_x, start_y) = max_coordinates

        whole_player_img = Cv2File.load_image(f'Wiki/Player/player_{position_direction}.png')

        height, width = whole_player_img.shape

        end_x = start_x + width
        end_y = start_y + height

        return start_x, start_y, end_x, end_y, position_direction

    @staticmethod
    def number(confidence: float, number_roi: np.array) -> int:
        number_coincidence = [(0, 0)]

        for number in range(10):
            number_image = Cv2File.load_image(f'Wiki/Number/{number}.png')

            match = cv2.matchTemplate(number_image, number_roi, cv2.TM_CCOEFF_NORMED)

            [_, max_coincidence, _, _] = cv2.minMaxLoc(match)

            if Scanner.__ensure_confidence_threshold(confidence, max_coincidence):
                continue

            if Scanner.__is_not_better_match(number_coincidence, max_coincidence):
                continue

            number_coincidence.remove(number_coincidence[0])

            number_coincidence.append((max_coincidence, number))

        if not number_coincidence:
            raise ImageIsNotNumber

        if Scanner.__ensure_some_match(coincidence_found=number_coincidence[0][0]):
            raise ImageIsNotNumber

        return number_coincidence[0][1]

    @staticmethod
    def __ensure_confidence_threshold(client_provided_confidence: float, coincidence_found: float) -> bool:
        return coincidence_found < client_provided_confidence

    @staticmethod
    def __ensure_some_match(coincidence_found: float) -> bool:
        return coincidence_found <= 0.5

    @staticmethod
    def __is_not_better_match(number_coincidence: list[tuple[any, int]], coincidence_found: float) -> bool:
        return number_coincidence[0][0] > coincidence_found
