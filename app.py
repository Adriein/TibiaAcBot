import keyboard
import pyautogui
from LoggerPackage import Logger as TibiaAcBotLogger

class TibiaAcBot:
    def init(self):
        TibiaAcBotLogger.log('Started...')
        TibiaAcBotLogger.log('Press space to finish the execution')

        while True:
            TibiaAcBotLogger.log('Listening...')

            if self.sigint():
                TibiaAcBotLogger.log('Graceful shutdown')
                break

    def sigint(self) -> bool:
        event = keyboard.read_event()
        return event.event_type == keyboard.KEY_DOWN and event.name == 'space'


app = TibiaAcBot()

app.init()
