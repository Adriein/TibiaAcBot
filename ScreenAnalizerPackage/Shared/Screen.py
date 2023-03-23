import pyautogui
import subprocess
import shlex
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Monitor import Monitor
from ScreenAnalizerPackage.Error.WindowSearchCommandError import WindowSearchCommandError
from UtilPackage.Array import Array


class Screen:
    MONITOR = None
    WINDOW_NAME = "Tibia"
    WINDOW_ID = None

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
    def __window_id() -> int:
        args = shlex.split(fr'xdotool search --name "\b"{Screen.WINDOW_NAME}"\b"')

        process = subprocess.run(args, stdout=subprocess.PIPE, text=True)

        try:
            process.check_returncode()
        except subprocess.CalledProcessError:
            raise WindowSearchCommandError(Screen.WINDOW_NAME)

        result = list(filter(None, process.stdout.split('\n')))

        if Array.is_array(result):
            for window_id in result:
                args = shlex.split(f'xdotool getwindowpid {window_id}')
                process = subprocess.run(args, stdout=subprocess.PIPE, text=True)
                print(process)

                # use pwdx <pid> to know if it's a process or not

        return 0

    @staticmethod
    def setup_global_variables() -> None:

        Screen.MONITOR = Screen.__size()

        Screen.WINDOW_ID = Screen.__window_id()
