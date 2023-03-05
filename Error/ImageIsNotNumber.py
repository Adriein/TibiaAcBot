class ImageIsNotNumber(BaseException):
    def __init__(self):
        super(ImageIsNotNumber, self).__init__("Image provided is not a number")
