from ConsolePackage import Console
from ScreenAnalizerPackage import Screen
from ScreenAnalizerPackage import Coordinate
from Xlib import X, display
from Xlib.ext import xtest


class Mouse:
    @staticmethod
    def use_left_button(coordinate: Coordinate) -> None:
        # Create a connection to the X server
        disp = display.Display()

        # Get the root window
        root = disp.screen().root

        tibia_window = disp.create_resource_object('window', Screen.TIBIA_WINDOW_ID)

        # Get the current pointer position
        original_pointer = root.query_pointer()

        # Move the pointer to a new location
        root.warp_pointer(coordinate.x, coordinate.y)

        # Send a left-click event
        xtest.fake_input(disp, X.ButtonPress, 1)
        disp.sync()
        xtest.fake_input(disp, X.ButtonRelease, 1)
        disp.sync()

        # Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {coordinate.x} {coordinate.y}')
        # Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
