from ConsolePackage.Console import Console
from Xlib import X, display, XK
from Xlib.protocol import event
from ScreenAnalizerPackage import Screen


class Keyboard:
    @staticmethod
    def press(key: str):
        # Create a connection to the X server
        d = display.Display()

        # Get the target window using its ID
        window = d.create_resource_object('window', Screen.TIBIA_WINDOW_ID)

        keycode = d.keysym_to_keycode(XK.string_to_keysym(key))
        key_event = X.KeyEvent(
            time=X.CurrentTime,
            root=d.screen().root,
            window=Screen.TIBIA_WINDOW_ID,
            same_screen=0,
            child=X.NONE,
            root_x=0,
            root_y=0,
            event_x=0,
            event_y=0,
            state=0,
            detail=keycode
        )

        d.screen().root.send_event(key_event, propagate=True)

        # flush the display to make sure the event is sent immediately
        display.flush()

        # Sync to make sure the event is processed
        d.sync()
        # Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
