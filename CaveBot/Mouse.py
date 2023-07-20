from ScreenAnalizerPackage import Coordinate
import pyautogui


class Mouse:
    def use_right_button(self, coordinate: Coordinate) -> None:
        pyautogui.moveTo(coordinate.x, coordinate.y)

        pyautogui.click(button='right')

    def use_left_button(self, coordinate: Coordinate) -> None:
        pyautogui.moveTo(coordinate.x, coordinate.y)

        pyautogui.click(button='left')
