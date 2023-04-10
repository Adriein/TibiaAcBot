from CaveBot.Player import Player
from ScreenAnalizerPackage import ScreenRegion
from ScreenAnalizerPackage import Position
from ScreenAnalizerPackage import PositionError
from threading import Event
from FilesystemPackage import Cv2File
from queue import Queue
import queue
import numpy as np
import cv2


class AutoLoot:
    def __init__(self, player: Player):
        self.player = player

    def loot(self, frame_queue: Queue, stop_walk_event: Event, processed_frame_queue: Queue) -> None:
        while True:
            frame = frame_queue.get()

            try:
                if not stop_walk_event.is_set():
                    processed_frame_queue.put(frame)
                    return

                position = self.player.position(frame)

                cv2.rectangle(frame, (position.start_x, position.start_y), (position.end_x, position.end_y), (255, 0, 0), 1)

                grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                looting_area = self.__create_looting_area(position)

                cv2.rectangle(frame, (looting_area.start_x, looting_area.start_y), (looting_area.end_x, looting_area.end_y), (255, 0, 0), 1)

                roi_looting_area = grey_scale_frame[looting_area.start_y: looting_area.end_y, looting_area.start_x: looting_area.end_x]

                corpse_template = Cv2File.load_image('Wiki/Ui/Battle/Mobs/MountainTroll/mountain_troll_corpse.png')

                match = cv2.matchTemplate(roi_looting_area, corpse_template, cv2.TM_CCOEFF_NORMED)

                [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

                # match_locations = (y_match_coords, x_match_coords) >= similarity more than threshold
                match_locations = np.where(match >= 0.9)

                # paired_match_locations = [(x, y), (x, y)]
                paired_match_locations = list(zip(*match_locations[::-1]))

                (start_x, start_y) = max_coordinates

                end_x = start_x + corpse_template.shape[1]
                end_y = start_y + corpse_template.shape[0]

                processed_frame_queue.put(frame)
            except PositionError:
                processed_frame_queue.put(frame)

            except Exception as exception:
                print(exception)

    def __create_looting_area(self, player_position: Position) -> ScreenRegion:
        start_x = player_position.start_x - 40
        end_x = player_position.end_x + 40
        start_y = player_position.start_y - 40
        end_y = player_position.end_y + 40

        return ScreenRegion(start_x, end_x, start_y, end_y)
