import subprocess
import shlex
from ScreenAnalizerPackage.Shared.Screen import Screen


class Keyboard:
    @staticmethod
    def press(key: str):
        args = shlex.split(f'xdotool search --name "{Screen.WINDOW_NAME}"')
        process = subprocess.run(args)
