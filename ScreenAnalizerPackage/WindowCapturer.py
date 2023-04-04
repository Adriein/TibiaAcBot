import numpy as np
from ScreenAnalizerPackage.Shared.Screen import Screen
from Xlib import display, X
from PIL import Image
import cv2


class WindowCapturer:
    IMAGE_MODE = 'RGB'
    DECODER = 'raw'
    ORDER = 'BGRX'
    @staticmethod
    def start() -> np.array:
        # Create a connection to the X server
        disp = display.Display()

        # Get the specified window
        window = disp.create_resource_object('window', Screen.OBS_TIBIA_PREVIEW_WINDOW_ID)

        # Get the dimensions of the window
        width = window.get_geometry().width
        height = window.get_geometry().height

        # Get the raw image data from the window
        raw = window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)

        # Convert the raw image data to a PIL Image object
        image = Image.frombytes(
            WindowCapturer.IMAGE_MODE,
            (width, height),
            raw.data,
            WindowCapturer.DECODER,
            WindowCapturer.ORDER
        )

        disp.close()

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
