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

        # Get the geometry of the target window
        geometry = tibia_window.get_geometry()

        # Translate the coordinates of the target window to coordinates relative to the root window
        tibia_window_coords = root.translate_coords(tibia_window, geometry.x, geometry.y)

        # Get the current pointer position
        original_pointer = root.query_pointer()

        # Move the pointer to the target position
        root.warp_pointer(original_pointer.root_x + coordinate.x - tibia_window_coords.x, original_pointer.root_y + coordinate.y - tibia_window_coords.y)

        # Send a left-click event
        xtest.fake_input(disp, X.ButtonPress, 1, X.NONE, 0, 0, 0)
        disp.sync()

        xtest.fake_input(disp, X.ButtonRelease, 1, X.NONE, 0, 0, 0)
        disp.sync()

        # Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {coordinate.x} {coordinate.y}')
        # Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
