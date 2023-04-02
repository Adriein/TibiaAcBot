from ScreenAnalizerPackage.Shared.Screen import Screen
from ScreenAnalizerPackage.Scanner import Scanner
from ScreenAnalizerPackage import PositionError
import cv2
from FilesystemPackage import File


class Position:
    @staticmethod
    def create() -> 'Position':
        try:
            actual_position = Screen.screenshot()

            (start_x, start_y, end_x, end_y, direction) = Scanner.player_position(
                screenshot=actual_position,
                confidence=0.9
            )

            # Position.__clean_tmp_folder()

            if cv2.waitKey(1):
                cv2.destroyAllWindows()

                # draw the bounding box on the image
            cv2.rectangle(actual_position, (start_x, start_y), (end_x, end_y), (255, 0, 0), 1)
            # show the output image
            cv2.imshow("Output", actual_position)
            cv2.waitKey(0)

            raise Exception

            return Position(start_x, start_y, end_x, end_y, direction)
        except Exception as exception:
            # Position.__clean_tmp_folder()

            raise PositionError(str(exception))

    @staticmethod
    def __clean_tmp_folder() -> None:
        File.delete_png('Tmp/PlayerPosition')

    def __init__(self, start_x, start_y, end_x, end_y, direction: str):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.direction = direction
