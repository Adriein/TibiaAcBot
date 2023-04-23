from ConsolePackage.Console import Console
from Xlib import X, display, Xutil
from Xlib.protocol import event
from ScreenAnalizerPackage import Screen

class Keyboard:
    @staticmethod
    def press(key: str):
        # Create a connection to the X server
        d = display.Display()

        # Get the target window using its ID
        window = d.create_resource_object('window', Screen.TIBIA_WINDOW_ID)

        keycode = Xutil.lookup_keysym(key)
        keypress_event = event.KeyPress(
            time=X.CurrentTime,
            root=window.get_root_window(),
            window=window,
            same_screen=X.SameScreen,
            child=X.NONE,
            root_x=0,
            root_y=0,
            event_x=0,
            event_y=0,
            state=0,
            detail=keycode
        )

        # Send the key event to the target window without focusing it
        window.send_event(keypress_event, X.SubstructureRedirectMask | X.SubstructureNotifyMask)

        # Sync to make sure the event is processed
        d.sync()
        #Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
