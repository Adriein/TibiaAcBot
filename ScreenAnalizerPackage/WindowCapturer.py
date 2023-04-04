import numpy as np
from ScreenAnalizerPackage.Shared.Screen import Screen


class WindowCapturer:
    @staticmethod
    def start() -> np.array:
        return Screen.window_capture(Screen.OBS_TIBIA_PREVIEW_WINDOW_ID)
