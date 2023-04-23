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

        # Get the keycode for the letter 'a'
        keycode = d.keysym_to_keycode(Xutil.lookup_keysym(key))

        # Send a KeyPress event to the target window without focusing it
        key_press_event = event.KeyPress(
            time=X.CurrentTime,
            root=window.get_geometry().root,
            window=window,
            same_screen=1,
            child=X.NONE,
            root_x=0,
            root_y=0,
            event_x=0,
            event_y=0,
            state=0,
            detail=keycode
        )

        key_press_event.send_event(window, event.ProperterMask.NoPropagate)

        # Send a KeyRelease event to the target window without focusing it
        key_release_event = event.KeyRelease(
            time=X.CurrentTime,
            root=window.get_geometry().root,
            window=window,
            same_screen=1,
            child=X.NONE,
            root_x=0,
            root_y=0,
            event_x=0,
            event_y=0,
            state=0,
            detail=keycode
        )
        key_release_event.send_event(window, event.ProperterMask.NoPropagate)

        # Sync to make sure the event is processed
        d.sync()
        # Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
