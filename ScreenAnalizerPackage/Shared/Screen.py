from io import BytesIO
import cv2
import pyautogui
from PIL import Image
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Monitor import Monitor
from ScreenAnalizerPackage.Error.WindowSearchCommandError import WindowSearchCommandError
from UtilPackage.Array import Array
from ConsolePackage.Console import Console
from ConsolePackage.CommandExecutionError import CommandExecutionError
from LoggerPackage.Logger import Logger
import numpy as np


class Screen:
    MONITOR = None
    TIBIA_WINDOW_NAME = "Tibia"
    OBS_TIBIA_PREVIEW_WINDOW_NAME = "Windowed Projector"
    TIBIA_WINDOW_ID = None
    OBS_TIBIA_PREVIEW_WINDOW_ID = None
    TIBIA_PID_BIN_PATH = "gmbh/tibia/packages/tibia/bin"

    @staticmethod
    def window_capture() -> np.array:
        stdout = Console.execute(f'import -window {Screen.TIBIA_WINDOW_ID} -silent png:-', text=False)

        image = Image.open(BytesIO(stdout))

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def screenshot() -> np.ndarray:
        return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def roi_screenshot(path: str, region: ScreenRegion) -> None:
        pyautogui.screenshot(path, region=(
            region.left,
            region.top,
            region.width,
            region.height
        ))

    @staticmethod
    def move_roi_pointer_left(pixels: int | float, region: ScreenRegion) -> ScreenRegion:
        return ScreenRegion(
            region.left - pixels,
            region.top,
            region.width,
            region.height
        )

    @staticmethod
    def move_roi_pointer_right(pixels: int | float, region: ScreenRegion) -> ScreenRegion:
        return ScreenRegion(
            region.left + pixels,
            region.top,
            region.width,
            region.height
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
            window_ids = Console.execute(fr'xdotool search --name "\b"{Screen.OBS_TIBIA_PREVIEW_WINDOW_NAME}"\b"')
            print(window_ids)
            window_ids_parsed_result = list(filter(None, window_ids.split('\n')))

            return 1

        except Exception as exception:
            Logger.error(str(exception), exception)
            raise WindowSearchCommandError(Screen.TIBIA_WINDOW_NAME)

    @staticmethod
    def setup_global_variables() -> None:

        Screen.MONITOR = Screen.__size()

        Screen.TIBIA_WINDOW_ID = Screen.__tibia_window_id()

        Screen.OBS_TIBIA_PREVIEW_WINDOW_ID = Screen.__obs_tibia_preview_window_id()
