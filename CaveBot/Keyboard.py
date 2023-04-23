from ConsolePackage.Console import Console
from Xlib import X, display
from Xlib.ext import xtest


class Keyboard:
    @staticmethod
    def press(key: str):
        # Create a connection to the X server
        d = display.Display()

        # Get the window ID of the target window
        window_id = 0x12345678

        # Get the target window using its ID
        window = d.create_resource_object('window', window_id)

        # Create a fake key event
        key_event = xtest.fake_input(d, X.KeyPress, ord(key))

        # Send the key event to the target window without focusing it
        window.send_event(key_event, X.SubstructureRedirectMask | X.SubstructureNotifyMask)

        # Sync to make sure the event is processed
        d.sync()
        # Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
