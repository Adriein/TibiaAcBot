from io import BytesIO

import cv2
import numpy as np
import pyautogui
from PIL import Image

from ConsolePackage.CommandExecutionError import CommandExecutionError
from ConsolePackage.Console import Console
from LoggerPackage.Logger import Logger
from ScreenAnalizerPackage.Error.WindowSearchCommandError import WindowSearchCommandError
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Monitor import Monitor
from UtilPackage.Array import Array
from FilesystemPackage import Cv2File


class Screen:
    MONITOR = None
    TIBIA_WINDOW_NAME = "Tibia"
    OBS_TIBIA_PREVIEW_WINDOW_NAME = "Projector"
    TIBIA_WINDOW_ID = None
    OBS_TIBIA_PREVIEW_WINDOW_ID = None
    TIBIA_PID_BIN_PATH = "gmbh/tibia/packages/tibia/bin"
    GAME_WINDOW = None

    @staticmethod
    def screenshot() -> np.ndarray:
        stdout = Console.execute(f'import -window {Screen.OBS_TIBIA_PREVIEW_WINDOW_ID} -silent png:-', text=False)

        image = Image.open(BytesIO(stdout))

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def move_roi_pointer_right(pixels: int | float, region: ScreenRegion) -> ScreenRegion:
        return ScreenRegion(
            start_x=region.start_x + pixels,
            end_x=region.start_x + pixels + 8,
            start_y=region.start_y,
            end_y=region.end_y
        )

    @staticmethod
    def __size() -> Monitor:
        [width, height] = pyautogui.size()

        return Monitor(width, height)

    @staticmethod
    def __tibia_window_id() -> int:
        try:
            window_ids = Console.execute(fr'xdotool search --name "\b"{Screen.TIBIA_WINDOW_NAME}"\b"')
            window_ids_parsed_result = list(filter(None, window_ids.split('\n')))

            if Array.is_array(window_ids_parsed_result):
                for window_id in window_ids_parsed_result:
                    try:
                        window_pid = Console.execute(f'xdotool getwindowpid {window_id}')

                        pid_info = Console.execute(f'pwdx {window_pid}')

                        if Screen.TIBIA_PID_BIN_PATH in pid_info.lower():
                            return int(window_id)

                    except CommandExecutionError:
                        continue

        except Exception as exception:
            Logger.error(str(exception), exception)
            raise WindowSearchCommandError(Screen.TIBIA_WINDOW_NAME)

    @staticmethod
    def __obs_tibia_preview_window_id() -> int:
        try:
            window_id = Console.execute(fr'xdotool search --name "\b"{Screen.OBS_TIBIA_PREVIEW_WINDOW_NAME}"\b"')

            if not window_id:
                raise Exception

            return int(window_id)

        except Exception as exception:
            Logger.error(str(exception), exception)
            raise WindowSearchCommandError(Screen.OBS_TIBIA_PREVIEW_WINDOW_NAME)

    @staticmethod
    def __game_window_location() -> ScreenRegion:
        frame = Screen.screenshot()
        left_game_window_arrow = Cv2File.load_image(f'Wiki/Ui/GameWindow/left_game_window_arrow.png')
        right_game_window_arrow = Cv2File.load_image(f'Wiki/Ui/GameWindow/right_game_window_arrow.png')

        match = cv2.matchTemplate(frame, left_game_window_arrow, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        match = cv2.matchTemplate(frame, right_game_window_arrow, cv2.TM_CCOEFF_NORMED)

        (left_arrow_start_x, left_arrow_start_y) = max_coordinates

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (right_arrow_start_x, right_arrow_start_y) = max_coordinates

        left_arrow_height, left_arrow_width = left_game_window_arrow.shape
        _, right_arrow_width = right_game_window_arrow.shape

        start_x = left_arrow_start_x + 140
        end_x = right_arrow_start_x - 130
        start_y = left_arrow_start_y
        end_y = left_arrow_start_y + left_arrow_height

        if cv2.waitKey(1):
            cv2.destroyAllWindows()

        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 1)
        # show the output image
        cv2.imshow("Output", frame)
        cv2.waitKey(0)

        return ScreenRegion(x, y, 960, 704)

    @staticmethod
    def setup_global_variables() -> None:

        Screen.MONITOR = Screen.__size()

        Screen.TIBIA_WINDOW_ID = Screen.__tibia_window_id()

        Screen.OBS_TIBIA_PREVIEW_WINDOW_ID = Screen.__obs_tibia_preview_window_id()

        Screen.GAME_WINDOW = Screen.__game_window_location()
