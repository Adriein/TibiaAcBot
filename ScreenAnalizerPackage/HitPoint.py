import pyautogui
from .Scanner import Scanner
from .ScreenRegion import ScreenRegion


class HitPoint:
    @staticmethod
    def get() -> int:
        hitpointLabelLocation = pyautogui.locateOnScreen(
            'Wiki/Stat/hp.png',
            confidence=0.8,
            grayscale=True,
            region=(1549, 74, 500, 1000)
        )

        print(Scanner.number(
            ScreenRegion(
                hitpointLabelLocation.left,
                hitpointLabelLocation.top,
                150,
                20
            )
        ))

        return 0
