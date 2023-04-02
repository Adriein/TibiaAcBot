import cv2
from glob import glob
from datetime import datetime
from ScreenAnalizerPackage.Error.ImageIsNotNumber import ImageIsNotNumber
from ScreenAnalizerPackage.Shared.Screen import Screen
from FilesystemPackage import Cv2File


class Scanner:
    @staticmethod
    def player(confidence: float):
        Screen.screenshot(f'Tmp/PlayerPosition/{datetime.now()}.png')

        player_position_templates = glob('Wiki/Player/*.png')

        [actual_position_screenshot_path] = glob('Tmp/PlayerPosition/*.png')

        actual_position = Cv2File.load_image(actual_position_screenshot_path)

        start_x = 0
        start_y = 0

        end_x = 0
        end_y = 0

        for position_path in player_position_templates:
            position_template = Cv2File.load_image(position_path)

            match = cv2.matchTemplate(actual_position, position_template, cv2.TM_CCOEFF_NORMED)

            [_, max_coincidence, _, max_coordinates] = cv2.minMaxLoc(match)

            if Scanner.__ensure_confidence_threshold(confidence, max_coincidence):
                continue

            (start_x, start_y) = max_coordinates

            end_x = start_x + position_template.shape[1]
            end_y = start_y + position_template.shape[0]

            print(max_coincidence)
            print(position_path)

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

        # draw the bounding box on the image
        cv2.rectangle(actual_position, (start_x, start_y), (end_x, end_y), (255, 0, 0), 1)
        # show the output image
        cv2.imshow("Output", actual_position)
        cv2.waitKey(0)
        raise Exception

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
