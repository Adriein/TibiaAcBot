import os
from glob import glob
from LoggerPackage import Logger


class File:
    @staticmethod
    def delete_png(path: str) -> None:
        images = glob(f'{path}/*.png', recursive=False)

        for image in images:
            try:
                os.remove(image)
            except OSError:
                Logger.error(OSError.strerror)
                raise OSError
