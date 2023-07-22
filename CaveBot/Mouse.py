from ScreenAnalizerPackage import Coordinate
import pyautogui


class Mouse:
    def use_right_button(self, coordinate: Coordinate) -> None:
        py_auto_gui_y = (coordinate.y * -1) - 768/2
        py_auto_gui_x = coordinate.x + 1366/2

        pyautogui.moveTo(py_auto_gui_x, py_auto_gui_y)

        pyautogui.click(button='right')

    def use_left_button(self, coordinate: Coordinate) -> None:
        pyautogui.moveTo(coordinate.x, coordinate.y)

        pyautogui.click(button='left')
