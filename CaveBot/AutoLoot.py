from CaveBot.Player import Player
from ScreenAnalizerPackage import ScreenRegion
from ScreenAnalizerPackage import Position
from FilesystemPackage import Cv2File
import numpy as np
import cv2


class AutoLoot:
    def __int__(self, player: Player):
        self.player = player

    def loot(self, frame: np.array) -> None:
        position = self.player.position(frame)

        roi_looting_area = self.__create_looting_area(position)

        corpse_template = Cv2File.load_image('Wiki/')

        cv2.matchTemplate(roi_looting_area, corpse_template, cv2.TM_CCOEFF_NORMED)



    def __create_looting_area(self, player_position: Position) -> ScreenRegion:
        start_x = player_position.start_x - 40
        end_x = player_position.end_x + 40
        start_y = player_position.start_y - 40
        end_y = player_position.end_y + 40

        return ScreenRegion(start_x, end_x, start_y, end_y)
