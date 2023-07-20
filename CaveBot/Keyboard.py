import pyautogui


class Keyboard:
    @staticmethod
    def press(key: str):
        pyautogui.press(key)

    @staticmethod
    def key_down(key: str) -> None:
        pyautogui.keyDown(key)

    @staticmethod
    def key_up(key: str) -> None:
        pyautogui.keyUp(key)
