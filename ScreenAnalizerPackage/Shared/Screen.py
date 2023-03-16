import pyautogui
from ScreenAnalizerPackage.ScreenRegion import ScreenRegion
from ScreenAnalizerPackage.Shared.Monitor import Monitor


class Screen:
    MONITOR = None

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
    def size() -> Monitor:
        [width, height] = pyautogui.size()

        return Monitor(width, height)

    @staticmethod
    def setup_global_variables() -> None:

        [width, height] = pyautogui.size()

        Screen.MONITOR = Monitor(width, height)
