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
from Xlib import display, X


class Screen:
    MONITOR = None
    TIBIA_WINDOW_NAME = "Tibia"
    OBS_TIBIA_PREVIEW_WINDOW_NAME = "Projector"
    TIBIA_WINDOW_ID = None
    OBS_TIBIA_PREVIEW_WINDOW_ID = None
    TIBIA_PID_BIN_PATH = "gmbh/tibia/packages/tibia/bin"

    @staticmethod
    def window_capture(window_id: int) -> np.array:
        # connect to the X11 display
        disp = display.Display()

        # get the window by ID
        window = disp.create_resource_object('window', window_id)

        # get the window size and position
        geometry = window.get_geometry()

        # create a pixmap to hold the window contents
        pixmap = disp.create_pixmap(
            window.root_depth,
            window_id,
            geometry.width,
            geometry.height
        )

        # copy the window contents into the pixmap
        disp.flush()
        disp.copy_area(window_id, pixmap, disp.get_default_gc(), 0, 0, geometry.width, geometry.height, 0, 0)

        # get the raw image data from the pixmap
        raw_image = pixmap.get_image(0, 0, geometry.width, geometry.height, X.ZPixmap, 0xffffffff)

        # convert the raw image data to a numpy array
        data = np.fromstring(raw_image.data, dtype=np.uint8)
        img_array = np.reshape(data, (geometry.height, geometry.width, 4))

        # convert the numpy array to a PIL image
        image = Image.fromarray(img_array, 'RGBA')

        # close the pixmap and X11 display
        pixmap.free()
        disp.close()

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def screenshot() -> np.ndarray:
        stdout = Console.execute(f'import -window {Screen.TIBIA_WINDOW_ID} -silent png:-', text=False)

        image = Image.open(BytesIO(stdout))

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

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
            window_id = Console.execute(fr'xdotool search --name "\b"{Screen.OBS_TIBIA_PREVIEW_WINDOW_NAME}"\b"')

            if not window_id:
                raise Exception

            return int(window_id)

        except Exception as exception:
            Logger.error(str(exception), exception)
            raise WindowSearchCommandError(Screen.OBS_TIBIA_PREVIEW_WINDOW_NAME)

    @staticmethod
    def setup_global_variables() -> None:

        Screen.MONITOR = Screen.__size()

        Screen.TIBIA_WINDOW_ID = Screen.__tibia_window_id()

        Screen.OBS_TIBIA_PREVIEW_WINDOW_ID = Screen.__obs_tibia_preview_window_id()
