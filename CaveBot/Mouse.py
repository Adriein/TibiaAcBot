from ScreenAnalizerPackage import Coordinate
import pyautogui


class Mouse:
    def move(self, coordinate: Coordinate) -> None:
        py_auto_gui_y = (coordinate.y * -1) + 768 / 2
        py_auto_gui_x = coordinate.x + 1366 / 2

        pyautogui.moveTo(coordinate.x, coordinate.y)
    def use_right_button(self) -> None:
        pyautogui.click(button='right')

    def use_left_button(self) -> None:
        pyautogui.click(button='left')
