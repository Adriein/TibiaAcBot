from ScreenAnalizerPackage import Screen
from ScreenAnalizerPackage import Coordinate
from Xlib import X, display
from Xlib.ext import xtest


class Mouse:
    LEFT_MOUSE_BUTTON = 1
    RIGHT_MOUSE_BUTTON = 3

    def __init__(self):
        # Create a connection to the X server
        self.disp = display.Display()

        # Get the root window
        self.root_window = self.disp.screen().root

        self.tibia_window = self.disp.create_resource_object('window', Screen.TIBIA_WINDOW_ID)

        # Get the geometry of the target window
        geometry = self.tibia_window.get_geometry()

        # Get the geometry of the root window
        root_geometry = self.root_window.get_geometry()

        # Translate the coordinates of the target window to coordinates relative to the root window
        tibia_window_coords = self.root_window.translate_coords(self.tibia_window, geometry.x, geometry.y)

        # Calculate the offset between the root window and the child window
        x_offset = geometry.x - root_geometry.x
        y_offset = geometry.y - root_geometry.y

        self.fixed_coordinate_x = tibia_window_coords.x - x_offset
        self.fixed_coordinate_y = tibia_window_coords.y - y_offset

    def use_right_button(self, coordinate: Coordinate) -> None:
        self.__move_mouse(coordinate)

        # Send a right-click event
        xtest.fake_input(self.disp, X.ButtonPress, self.RIGHT_MOUSE_BUTTON, X.NONE)
        self.disp.sync()

        xtest.fake_input(self.disp, X.ButtonRelease, self.RIGHT_MOUSE_BUTTON, X.NONE)
        self.disp.sync()

    def use_left_button(self, coordinate: Coordinate) -> None:
        self.__move_mouse(coordinate)

        # Send a left-click event
        xtest.fake_input(self.disp, X.ButtonPress, self.LEFT_MOUSE_BUTTON, X.NONE)
        self.disp.sync()

        xtest.fake_input(self.disp, X.ButtonRelease, self.LEFT_MOUSE_BUTTON, X.NONE)
        self.disp.sync()

    def __move_mouse(self, coordinate: Coordinate) -> None:
        # Move the pointer to the target position
        self.root_window.warp_pointer(self.fixed_coordinate_x + coordinate.x, self.fixed_coordinate_y + coordinate.y)
