import cv2
import re
import pyautogui
from glob import glob
from ScreenAnalizerPackage.Error.ImageIsNotNumber import ImageIsNotNumber
from FilesystemPackage import Cv2File
import numpy as np


class Scanner:
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

        end_x = 0
        end_y = 0

        position_direction = None

        for position_path in player_position_templates:
            position_template = Cv2File.load_image(position_path)

            match = cv2.matchTemplate(grey_scale_frame, position_template, cv2.TM_CCOEFF_NORMED)

            [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

            if Scanner.__ensure_confidence_threshold(confidence, max_coincidence):
                continue

            position_direction = re.search(r'(?<=/)\w+(?=\.)', position_path).group(0)

            (start_x, start_y) = max_coordinates

            end_x = start_x + position_template.shape[1]
            end_y = start_y + position_template.shape[0]

        whole_player_img = Cv2File.load_image(f'Wiki/Player/player_{position_direction}.png')

        y, x = whole_player_img.shape

        return start_x, start_y, end_x + x, end_y + y, position_direction

    @staticmethod
    def number(confidence: float, template_path: str) -> int:
        number_coincidence = [(0, 0)]

        for number in range(10):
            number_image = Cv2File.load_image(f'Wiki/Number/{number}.png')

            [number_template_path] = glob(template_path)

            number_template = Cv2File.load_image(number_template_path)

            match = cv2.matchTemplate(number_image, number_template, cv2.TM_CCOEFF_NORMED)

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
