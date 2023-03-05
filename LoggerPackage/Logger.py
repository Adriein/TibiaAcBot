from UtilPackage import Time


class Logger:
    @staticmethod
    def info(message: str) -> None:
        print(f'[{Time.now()}][TibiaAcBot][INFO]: {message}')

    @staticmethod
    def debug(message: str) -> None:
        print(f'[{Time.now()}][TibiaAcBot][DEBUG]: {message}')

    @staticmethod
    def error(message: str) -> None:
        print(f'[{Time.now()}][TibiaAcBot][ERROR]: {message}')
