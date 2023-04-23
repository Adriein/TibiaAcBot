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

        keycode = XK.string_to_keysym(key)# d.keysym_to_keycode(XK.string_to_keysym(key))
        time = X.CurrentTime
        key_press_event = event.KeyPress(
            time=time,
            root=d.screen().root.id,
            window=Screen.TIBIA_WINDOW_ID,
            same_screen=0,
            child=X.PointerRoot,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=X.Mod1Mask,
            detail=keycode
        )
        window.send_event(key_press_event, propagate=True)

        key_release_event = event.KeyRelease(
            time=time,
            root=d.screen().root.id,
            window=Screen.TIBIA_WINDOW_ID,
            same_screen=0,
            child=X.PointerRoot,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=X.Mod1Mask,
            detail=keycode
        )
        window.send_event(key_release_event, propagate=True)

        # Sync to make sure the event is processed
        d.sync()
        # Console.execute(f'xdotool windowfocus --sync {Screen.TIBIA_WINDOW_ID} key {key}')
