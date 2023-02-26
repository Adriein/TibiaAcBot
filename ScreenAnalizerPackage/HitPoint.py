import pyautogui
from ScreenAnalizerPackage import Scanner, ScreenRegion


class HitPoint:
    @staticmethod
    def get() -> int:
        hitpointLabelLocation = pyautogui.locateOnScreen(
            'Wiki/Stat/hp.png',
            confidence=0.8,
            grayscale=True,
            region=(1549, 74, 500, 1000)
        )

        hitpointLabelLocationRightCorner = hitpointLabelLocation.left + hitpointLabelLocation.width

        return Scanner.number(
            ScreenRegion(
                hitpointLabelLocationRightCorner + 30,
                hitpointLabelLocation.top + 5,
                9,
                12
            )
        )
