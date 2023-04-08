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

        # Get the geometry of the root window
        root_geometry = root.get_geometry()

        # Translate the coordinates of the target window to coordinates relative to the root window
        tibia_window_coords = root.translate_coords(tibia_window, geometry.x, geometry.y)

        # Calculate the offset between the root window and the child window
        x_offset = geometry.x - root_geometry.x
        y_offset = geometry.y - root_geometry.y


        # Move the pointer to the target position
        root.warp_pointer(tibia_window_coords.x + coordinate.x - x_offset, tibia_window_coords.y + coordinate.y - y_offset)

        # Send a left-click event
        xtest.fake_input(disp, X.ButtonPress, 1, X.NONE, 0, 0, 0)
        disp.sync()

        xtest.fake_input(disp, X.ButtonRelease, 1, X.NONE, 0, 0, 0)
        disp.sync()

        # Console.execute(f'xdotool mousemove --window {Screen.TIBIA_WINDOW_ID} --sync {coordinate.x} {coordinate.y}')
        # Console.execute(f'xdotool click --window {Screen.TIBIA_WINDOW_ID} 1')
