from ConsolePackage.Console import Console
from Xlib import X, display
from Xlib.ext import xtest
from ScreenAnalizerPackage import Screen


class Keyboard:
    @staticmethod
    def press(key: str):
        # Create a connection to the X server
        d = display.Display()

        # Get the target window using its ID
        window = d.create_resource_object('window', Screen.TIBIA_WINDOW_ID)

        # Create a fake key event
        key_event = xtest.fake_input(d, X.KeyPress, ord(key))

        # Send the key event to the target window without focusing it
        window.send_event(key_event, X.SubstructureRedirectMask | X.SubstructureNotifyMask)

        # Sync to make sure the event is processed
        d.sync()
        # Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
