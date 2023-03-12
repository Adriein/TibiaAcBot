import traceback

from UtilPackage import Time
from UtilPackage import Array


class Logger:
    @staticmethod
    def info(message: str) -> None:
        print(f'[{Time.now()}][TibiaAcBot][INFO]: {message}')

    @staticmethod
    def debug(message: str) -> None:
        print(f'[{Time.now()}][TibiaAcBot][DEBUG]: {message}')

    @staticmethod
    def error(message: str, error: Exception) -> None:
        if not message:
            message = 'Fatal Exception without message'

        print(f'[{Time.now()}][TibiaAcBot][ERROR]: {message}')
        print(f'  [TibiaAcBot][TRACE]:')
        for index, stack_trace in enumerate(Array.reverse(traceback.format_tb(error.__traceback__))):
            stack_list = stack_trace.strip().replace("\n", "").split(",")
            print(f'    > [{index}] {stack_list[0]}')
            print(f'    > [{index}] {stack_list[1].strip()}')
            print(f'    > [{index}] {stack_list[2].strip()}')
            print("")
