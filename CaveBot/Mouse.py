from ScreenAnalizerPackage import Coordinate
import pyautogui


class Mouse:
    def move(self, coordinate: Coordinate) -> None:
        pyautogui.moveTo(coordinate.x + 20, coordinate.y)

    def use_right_button(self) -> None:
        pyautogui.click(button='right')

    def use_left_button(self) -> None:
        pyautogui.click(button='left')
